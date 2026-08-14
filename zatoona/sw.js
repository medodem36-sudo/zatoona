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
   fallback now happens inside the helper itself. */

const CACHE_VERSION = 'v2';
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
