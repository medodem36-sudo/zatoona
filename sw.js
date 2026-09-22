/* ================= زتونة — Service Worker =================
   Scope: PWA offline support ONLY. This file never reads or writes
   localStorage — all user data (meals, workouts, budget, schedule, notes,
   reminders, etc.) lives exclusively in the page's localStorage under the
   'meal-gym-tracker:' prefix and is completely untouched by anything here.

   Bump CACHE_VERSION on every real deploy. That's the only line that needs
   to change for a normal update — activate() cleans up the old versioned
   caches automatically and safely, and localStorage is never part of that
   cleanup because it isn't stored via the Cache Storage API at all.

   v2: added the /zatoona/ root ('./' and './index.html') to the shell so the
   PWA's actual start_url/scope entry point is precached and controlled —
   the v1 shell only precached gym-meal-tracker-6_8.html directly, which is
   why the root URL wasn't reliably available offline before. Also fixed a
   dead fallback: staleWhileRevalidate() never actually rejects (even its
   worst case resolves to Response.error()), so the old
   `.catch(() => caches.match(...))` at the call site could never run. The
   fallback now happens inside the helper itself.

   v3: Session 2 — index.html content changed substantially (Budget missing-
   price handling + the fully editable Schedule/Time-Engine). No shell asset
   paths changed, so SHELL_ASSETS below is untouched; bumping the version is
   the only thing needed to make the existing user-triggered update flow
   offer this new content next time the app checks.

   v4: Session 2 completion — Meal/Gym to future-Schedule sync (meal
   enabled/duration and gym-workout-duration now read from schedule-settings
   instead of fixed constants, reusing the existing edited-flag/materialization
   mechanism unchanged). Content-only change again; no shell asset paths
   changed.

   v5: Session 2.5 — Dynamic Daily Timeline / cascading schedule. Editing an
   activity's time now auto-shifts eligible FLEXIBLE activities after it to
   avoid stale overlaps, stopping at any FIXED (prayer/sleep/college/commute)
   or per-occurrence MANUAL (timeLocked) activity. Added Reset-to-Auto and
   Recalculate-Day controls. Purely additive to the activity data model
   (new optional timeLocked field); no shell asset paths changed.

   v6: Session 3 — Home/Navigation (new default landing screen + browser
   history), a schema-v2 migration fixing a Schedule/Budget recurring-defs
   key collision, several real XSS fixes (escaped user text that was going
   into innerHTML/attribute contexts unescaped), Backup/Restore shape
   validation before any data is written, and a data-safety pass making
   every JSON.parse from storage crash-proof (malformed or wrong-shape
   values now fall back safely instead of throwing during init). Content-
   only change; no shell asset paths changed.

   v7: Session 3.1 — CRITICAL HOTFIX: Dynamic Timeline delete-gap. Deleting
   a Schedule activity left a dead gap instead of pulling the following
   tightly-packed FLEXIBLE activities back to close it, and "Recalculate
   Day" could silently resurrect a this-occurrence delete. Added a scoped
   backward-compaction pass (compactGapAfterRemoval) that closes exactly
   the freed slot, walking forward only through activities that were
   originally contiguous, and stopping at the first FIXED/MANUAL wall or
   any pre-existing (legitimate, intentional) gap — so it never eats real
   free time elsewhere in the day. deleteActivity() now also records
   this-occurrence deletions (deletedGenKeys/deletedDefIds) so
   recalculateDay() excludes them instead of regenerating them from
   scratch. Verified idempotent (repeated Recalculate Day converges, no
   drift/duplicates), safe around FIXED/MANUAL walls and pre-existing free
   time, safe across midnight-adjacent activities, and a no-op byte-for-
   byte on every untouched/pristine day (checked against all 7 weekday
   templates). Content-only change; no shell asset paths changed. */

const CACHE_VERSION = 'v7';
const SHELL_CACHE = 'zatoona-shell-' + CACHE_VERSION;
const RUNTIME_CACHE = 'zatoona-runtime-' + CACHE_VERSION;
const CURRENT_CACHES = [SHELL_CACHE, RUNTIME_CACHE];

/* The exact app shell — same-origin files required for the app to load and
   run with zero network access. './' and './index.html' are the real PWA
   entry point (manifest start_url/scope); gym-meal-tracker-6_8.html is kept
   too since it's still a valid, directly-linkable working copy. */
const SHELL_ASSETS = [
  './',
  './index.html',
  './gym-meal-tracker-6_8.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/icon-apple-touch-180.png',
  './icons/favicon-32.png',
];
const SHELL_FALLBACK = './'; // what to serve for any in-scope navigation that isn't individually cached

/* Cross-origin hosts we opportunistically cache AFTER a successful fetch
   (never pre-fetched in bulk) — exercise photos + the optional web font.
   Nothing else external is cached; e.g. exrx.net article links and the
   science-source links in the Schedule tab are never touched here, since
   they're meant to open in a real browser tab, not be usable offline. */
const RUNTIME_HOSTS = [
  'commons.wikimedia.org',
  'fonts.googleapis.com',
  'fonts.gstatic.com',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_ASSETS))
      .catch((err) => {
        // Never let a single missing/renamed shell asset block installation —
        // the app must still install and work for everything that DID cache.
        console.warn('[sw] shell precache had an issue:', err);
      })
  );
  // Deliberately NOT calling self.skipWaiting() here — the page decides when
  // to activate a new version (see the SKIP_WAITING message handler below),
  // so a mid-session user is never yanked onto new code without warning.
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();
      await Promise.all(
        names
          .filter((n) => n.startsWith('zatoona-') && !CURRENT_CACHES.includes(n))
          .map((n) => caches.delete(n))
      );
      await self.clients.claim();
    })()
  );
});

// Lets the page trigger activation of a waiting service worker on its own
// schedule (see the update banner in the app), instead of this file forcing
// a reload on its own.
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

function isRuntimeHost(url) {
  return RUNTIME_HOSTS.some((h) => url.hostname === h);
}

/* Cache-first-on-miss-fallback for navigations/shell assets: try the exact
   cached match, then network (updating the cache for next time), then a
   named shell fallback (index/root) — all resolved INSIDE this function so
   there's no reliance on a rejected promise that never actually happens. */
async function staleWhileRevalidate(request, cacheName, fallbackUrl) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const networkPromise = fetch(request)
    .then((resp) => {
      if (resp && resp.ok) cache.put(request, resp.clone());
      return resp;
    })
    .catch(() => null);
  const fresh = await networkPromise;
  if (cached) return cached;
  if (fresh) return fresh;
  if (fallbackUrl) {
    const fallback = await cache.match(fallbackUrl);
    if (fallback) return fallback;
  }
  return Response.error();
}

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  try {
    const resp = await fetch(request);
    // Opaque (no-cors cross-origin) responses are still cacheable and usable as <img src>.
    if (resp && (resp.ok || resp.type === 'opaque')) cache.put(request, resp.clone());
    return resp;
  } catch (err) {
    return cached || Response.error();
  }
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return; // never touch writes

  const url = new URL(request.url);

  // Same-origin navigations and shell assets: stale-while-revalidate so the
  // app opens instantly from cache (works offline) while quietly picking up
  // updates in the background for next time.
  if (url.origin === self.location.origin) {
    const isShellAsset = SHELL_ASSETS.some((a) => {
      const assetPath = new URL(a, self.location.href).pathname;
      return url.pathname === assetPath;
    });
    if (request.mode === 'navigate' || isShellAsset) {
      event.respondWith(staleWhileRevalidate(request, SHELL_CACHE, SHELL_FALLBACK));
      return;
    }
    // Any other same-origin asset (e.g. icons requested directly): cache-first.
    event.respondWith(cacheFirst(request, SHELL_CACHE));
    return;
  }

  // Cross-origin: only the specific hosts we've allow-listed get opportunistic
  // runtime caching (exercise photos, the web font). Everything else (exrx.net,
  // CDC/WHO/journal source links, etc.) is left to the network/browser as normal —
  // those are reference links meant to be opened online, not offline assets.
  if (isRuntimeHost(url)) {
    event.respondWith(cacheFirst(request, RUNTIME_CACHE));
  }
  // No respondWith() call for anything else => default browser network behavior,
  // which fails gracefully offline exactly like a normal missing resource would.
});
