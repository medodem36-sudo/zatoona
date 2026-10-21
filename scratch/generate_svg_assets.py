# -*- coding: utf-8 -*-
import os

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
warmup_dir = os.path.join(repo, "assets", "images", "warmup")
cooldown_dir = os.path.join(repo, "assets", "images", "cooldown")
os.makedirs(warmup_dir, exist_ok=True)
os.makedirs(cooldown_dir, exist_ok=True)

# ----------------- WARMUP SVGS -----------------

# 1. Cardio / Jogging
svg_w1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <!-- Card Background -->
  <rect width="200" height="200" rx="16" fill="url(#bgGradW1)"/>
  <circle cx="100" cy="100" r="78" fill="none" stroke="#c8ecd7" stroke-width="2" stroke-dasharray="5 5"/>
  
  <!-- Pulse Rhythm Indicator -->
  <path d="M 24 38 L 44 38 L 50 25 L 58 50 L 66 30 L 72 40 L 88 38" fill="none" stroke="#e65100" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Ground Motion Track -->
  <line x1="30" y1="168" x2="170" y2="168" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>
  <line x1="45" y1="174" x2="115" y2="174" stroke="#81c784" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Motion Streaks Behind -->
  <path d="M 35 85 L 60 85 M 28 100 L 52 100 M 38 115 L 58 115" stroke="#81c784" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Male Athletic Runner -->
  <!-- Head -->
  <circle cx="126" cy="46" r="14" fill="url(#maleGrad)"/>
  <!-- Torso (athletic lean) -->
  <path d="M 124 58 L 108 106" stroke="url(#maleGrad)" stroke-width="14" stroke-linecap="round"/>
  <!-- Left Leg (Trailing extension) -->
  <path d="M 108 106 L 82 128 L 56 148" fill="none" stroke="url(#maleGrad)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 56 148 L 46 154" stroke="url(#maleGrad)" stroke-width="8" stroke-linecap="round"/>
  <!-- Right Leg (Forward high knee) -->
  <path d="M 108 106 L 132 122 L 118 158" fill="none" stroke="#2e7d32" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 118 158 L 134 164" stroke="#2e7d32" stroke-width="8" stroke-linecap="round"/>
  <!-- Left Arm (Backwards pump) -->
  <path d="M 118 72 L 96 86 L 84 76" fill="none" stroke="url(#maleGrad)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Right Arm (Forward drive) -->
  <path d="M 120 72 L 142 88 L 158 76" fill="none" stroke="#2e7d32" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# 2. Arm Circles
svg_w2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradW2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradW2)"/>
  
  <!-- Circular Motion Trajectories on both sides -->
  <!-- Left arm rotation circle -->
  <ellipse cx="44" cy="95" rx="26" ry="32" fill="none" stroke="#e65100" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="44,60 52,67 44,74" fill="#e65100"/>
  <!-- Right arm rotation circle -->
  <ellipse cx="156" cy="95" rx="26" ry="32" fill="none" stroke="#e65100" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="156,60 164,67 156,74" fill="#e65100"/>
  
  <!-- Male Athletic Figure Standing Frontal -->
  <!-- Head -->
  <circle cx="100" cy="42" r="15" fill="url(#maleGradW2)"/>
  <!-- Broad Shoulders & Torso -->
  <path d="M 72 74 Q 100 68 128 74 L 118 124 L 82 124 Z" fill="url(#maleGradW2)"/>
  <!-- Left Arm Extended -->
  <path d="M 76 74 L 46 92" stroke="url(#maleGradW2)" stroke-width="9" stroke-linecap="round"/>
  <!-- Right Arm Extended -->
  <path d="M 124 74 L 154 92" stroke="url(#maleGradW2)" stroke-width="9" stroke-linecap="round"/>
  <!-- Legs (solid stance) -->
  <path d="M 90 124 L 84 172" stroke="url(#maleGradW2)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 110 124 L 116 172" stroke="url(#maleGradW2)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 84 172 L 72 176 M 116 172 L 128 176" stroke="url(#maleGradW2)" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Rotational arrows badge -->
  <text x="100" y="190" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#1b5e20" text-anchor="middle">360° الدوران</text>
</svg>"""

# 3. Leg Swings
svg_w3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradW3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradW3)"/>
  
  <!-- Swing Arc Trajectory -->
  <path d="M 162 120 Q 150 166 100 170 Q 56 166 42 135" fill="none" stroke="#e65100" stroke-width="3" stroke-dasharray="6 4"/>
  <polygon points="162,116 166,128 156,124" fill="#e65100"/>
  <polygon points="42,132 40,144 50,140" fill="#e65100"/>

  <!-- Support Wall / Bar Post -->
  <line x1="38" y1="35" x2="38" y2="175" stroke="#a5d6a7" stroke-width="5" stroke-linecap="round"/>

  <!-- Male Athletic Figure in Profile Swing -->
  <!-- Hand on support bar -->
  <line x1="38" y1="84" x2="72" y2="82" stroke="url(#maleGradW3)" stroke-width="7" stroke-linecap="round"/>
  <!-- Head -->
  <circle cx="86" cy="46" r="14" fill="url(#maleGradW3)"/>
  <!-- Torso upright -->
  <path d="M 86 58 L 86 112" stroke="url(#maleGradW3)" stroke-width="13" stroke-linecap="round"/>
  <!-- Left Leg (Support standing straight) -->
  <path d="M 84 112 L 84 168" stroke="url(#maleGradW3)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 84 168 L 74 172" stroke="url(#maleGradW3)" stroke-width="7" stroke-linecap="round"/>
  <!-- Right Leg (Dynamic Swing Forward) -->
  <path d="M 88 112 L 126 130 L 156 122" fill="none" stroke="#2e7d32" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 156 122 L 168 118" stroke="#2e7d32" stroke-width="7" stroke-linecap="round"/>
  <!-- Free Arm balanced on hip -->
  <path d="M 88 74 L 104 86 L 96 102" fill="none" stroke="url(#maleGradW3)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# 4. Hip Circles / Pelvic Rotation
svg_w4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradW4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradW4)"/>
  
  <!-- Pelvic Rotational Ring & Arrows -->
  <ellipse cx="100" cy="116" rx="46" ry="16" fill="none" stroke="#e65100" stroke-width="3" stroke-dasharray="6 4"/>
  <polygon points="144,118 152,110 152,122" fill="#e65100"/>
  <polygon points="56,114 48,122 48,110" fill="#e65100"/>

  <!-- Male Athletic Figure Standing Hands on Hips -->
  <!-- Head -->
  <circle cx="100" cy="40" r="14" fill="url(#maleGradW4)"/>
  <!-- Torso -->
  <path d="M 76 68 Q 100 62 124 68 L 114 114 L 86 114 Z" fill="url(#maleGradW4)"/>
  <!-- Arms akimbo (hands on hips) -->
  <path d="M 78 68 L 56 90 L 82 108" fill="none" stroke="url(#maleGradW4)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 122 68 L 144 90 L 118 108" fill="none" stroke="url(#maleGradW4)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Legs (shoulder-width stance) -->
  <path d="M 90 114 L 78 166" stroke="url(#maleGradW4)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 110 114 L 122 166" stroke="url(#maleGradW4)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 78 166 L 66 170 M 122 166 L 134 170" stroke="url(#maleGradW4)" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Ground reference -->
  <line x1="50" y1="172" x2="150" y2="172" stroke="#a5d6a7" stroke-width="2" stroke-linecap="round"/>
</svg>"""

# 5. Bodyweight Squat (controlled)
svg_w5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradW5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradW5)"/>
  
  <!-- Down/Up Motion Arrows -->
  <path d="M 36 85 L 36 125" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="36,132 30,122 42,122" fill="#e65100"/>
  <polygon points="36,78 30,88 42,88" fill="#e65100"/>

  <!-- Male Athletic Figure in Parallel Squat -->
  <!-- Head -->
  <circle cx="106" cy="58" r="14" fill="url(#maleGradW5)"/>
  <!-- Torso (flat back, angled forward 45°) -->
  <path d="M 104 70 L 78 114" stroke="url(#maleGradW5)" stroke-width="14" stroke-linecap="round"/>
  <!-- Arms extended forward for balance -->
  <path d="M 100 80 L 148 80" stroke="url(#maleGradW5)" stroke-width="8" stroke-linecap="round"/>
  <!-- Thigh (Parallel to ground) -->
  <path d="M 78 114 L 126 116" stroke="url(#maleGradW5)" stroke-width="12" stroke-linecap="round"/>
  <!-- Shin (45° angle) -->
  <path d="M 126 116 L 114 166" stroke="url(#maleGradW5)" stroke-width="10" stroke-linecap="round"/>
  <!-- Foot flat on ground -->
  <path d="M 108 166 L 132 166" stroke="url(#maleGradW5)" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Ground Line -->
  <line x1="50" y1="168" x2="160" y2="168" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>
</svg>"""

# 6. Warmup Set (Barbell/Weight light set)
svg_w6 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradW6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradW6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0d3b13"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradW6)"/>
  
  <!-- Warmup Light Set Badge: 50% -->
  <rect x="22" y="24" width="58" height="24" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.5"/>
  <text x="51" y="40" font-family="'IBM Plex Mono', monospace, sans-serif" font-size="11" font-weight="bold" fill="#1b5e20" text-anchor="middle">50% W.T</text>

  <!-- Male Athletic Figure Lifting Barbell -->
  <!-- Head -->
  <circle cx="100" cy="48" r="14" fill="url(#maleGradW6)"/>
  <!-- Torso -->
  <path d="M 80 74 Q 100 68 120 74 L 112 120 L 88 120 Z" fill="url(#maleGradW6)"/>
  <!-- Arms holding barbell at chest level -->
  <path d="M 82 74 L 64 96 L 76 96" stroke="url(#maleGradW6)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 118 74 L 136 96 L 124 96" stroke="url(#maleGradW6)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Barbell with small warmup plates -->
  <line x1="30" y1="96" x2="170" y2="96" stroke="#455a64" stroke-width="5" stroke-linecap="round"/>
  <!-- Light small plates on sides -->
  <rect x="38" y="82" width="8" height="28" rx="2" fill="#78909c"/>
  <rect x="154" y="82" width="8" height="28" rx="2" fill="#78909c"/>

  <!-- Legs athletic stance -->
  <path d="M 92 120 L 82 168" stroke="url(#maleGradW6)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 108 120 L 118 168" stroke="url(#maleGradW6)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 82 168 L 70 172 M 118 168 L 130 172" stroke="url(#maleGradW6)" stroke-width="8" stroke-linecap="round"/>
  
  <line x1="45" y1="172" x2="155" y2="172" stroke="#a5d6a7" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

# ----------------- COOLDOWN SVGS -----------------

# 1. Shoulder Stretch (Cross-body)
svg_c1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC1)"/>
  
  <!-- Stretch Tension Highlight Arc -->
  <path d="M 135 65 Q 155 75 145 100" fill="none" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <polygon points="144,106 142,94 152,98" fill="#e65100"/>
  
  <!-- Male Athletic Figure Performing Shoulder Stretch -->
  <!-- Head -->
  <circle cx="100" cy="42" r="14" fill="url(#maleGradC1)"/>
  <!-- Torso -->
  <path d="M 76 70 Q 100 64 124 70 L 114 122 L 86 122 Z" fill="url(#maleGradC1)"/>
  <!-- Right Arm crossing horizontally over chest -->
  <path d="M 124 74 L 62 82" stroke="url(#maleGradC1)" stroke-width="9" stroke-linecap="round"/>
  <!-- Left Arm pulling right elbow gently toward body -->
  <path d="M 78 74 L 84 102 L 94 80" fill="none" stroke="#1e88e5" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Legs upright stance -->
  <path d="M 90 122 L 84 170" stroke="url(#maleGradC1)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 110 122 L 116 170" stroke="url(#maleGradC1)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 84 170 L 72 174 M 116 170 L 128 174" stroke="url(#maleGradC1)" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Duration Badge -->
  <rect x="20" y="24" width="58" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.5"/>
  <text x="49" y="39" font-family="'IBM Plex Mono', monospace, sans-serif" font-size="10" font-weight="bold" fill="#0d47a1" text-anchor="middle">20-30s</text>
</svg>"""

# 2. Chest Stretch (Wall / Doorway)
svg_c2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC2)"/>
  
  <!-- Wall / Door Post Reference -->
  <rect x="30" y="30" width="14" height="145" rx="3" fill="#90caf9" stroke="#64b5f6" stroke-width="1.5"/>
  
  <!-- Rotation arrow away from wall -->
  <path d="M 120 70 Q 145 78 152 98" fill="none" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <polygon points="154,104 148,94 158,96" fill="#e65100"/>

  <!-- Male Athletic Figure Stretching Pectorals -->
  <!-- Hand placed flat on wall at 90° -->
  <circle cx="37" cy="80" r="5" fill="url(#maleGradC2)"/>
  <!-- Left Arm bent at 90 degrees against wall -->
  <path d="M 37 80 L 65 80 L 86 82" fill="none" stroke="url(#maleGradC2)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Head turned slightly away -->
  <circle cx="106" cy="46" r="14" fill="url(#maleGradC2)"/>
  <!-- Torso gently rotated outward opening chest -->
  <path d="M 86 80 L 118 78 L 112 124 L 92 124 Z" fill="url(#maleGradC2)"/>
  <!-- Free Right Arm hanging naturally -->
  <path d="M 118 78 L 132 104" stroke="url(#maleGradC2)" stroke-width="8" stroke-linecap="round"/>
  <!-- Legs staggered stance for solid leverage -->
  <path d="M 96 124 L 88 170" stroke="url(#maleGradC2)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 110 124 L 126 166" stroke="url(#maleGradC2)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 88 170 L 76 172 M 126 166 L 138 168" stroke="url(#maleGradC2)" stroke-width="7" stroke-linecap="round"/>
</svg>"""

# 3. Lower Back & Glute Stretch (Supine Knee to Chest)
svg_c3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC3)"/>
  
  <!-- Exercise Mat on Floor -->
  <rect x="20" y="146" width="160" height="10" rx="4" fill="#bbdefb" stroke="#90caf9" stroke-width="1.5"/>

  <!-- Male Athletic Figure Lying Supine -->
  <!-- Head on mat -->
  <circle cx="44" cy="132" r="14" fill="url(#maleGradC3)"/>
  <!-- Back / Torso resting flat on mat -->
  <path d="M 58 138 L 112 138" stroke="url(#maleGradC3)" stroke-width="14" stroke-linecap="round"/>
  <!-- Left Leg extended straight along mat -->
  <path d="M 112 140 L 164 140" stroke="url(#maleGradC3)" stroke-width="9" stroke-linecap="round"/>
  <path d="M 164 140 L 174 136" stroke="url(#maleGradC3)" stroke-width="7" stroke-linecap="round"/>
  
  <!-- Right Leg pulled up: Knee to chest -->
  <path d="M 110 138 L 86 96 L 102 82" fill="none" stroke="#1e88e5" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Arms clasped around right knee pulling gently -->
  <path d="M 72 136 L 86 102 L 96 92" fill="none" stroke="url(#maleGradC3)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Stretch Arrow toward chest -->
  <path d="M 108 72 L 86 86" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="82,88 94,88 88,78" fill="#e65100"/>
</svg>"""

# 4. Hamstring Stretch (Seated reaching forward)
svg_c4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC4)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="156" x2="175" y2="156" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Forward reach stretch arrow -->
  <path d="M 88 78 L 134 100" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="140,103 128,103 133,93" fill="#e65100"/>

  <!-- Male Athletic Figure Seated on Floor -->
  <!-- Glutes / Pelvis seated on floor -->
  <!-- Left Extended Leg flat on floor -->
  <path d="M 68 148 L 152 148" stroke="url(#maleGradC4)" stroke-width="11" stroke-linecap="round"/>
  <!-- Foot flexed upward -->
  <path d="M 152 148 L 156 128" stroke="url(#maleGradC4)" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Head -->
  <circle cx="76" cy="74" r="14" fill="url(#maleGradC4)"/>
  <!-- Torso leaning forward from hips with flat back -->
  <path d="M 68 148 L 86 86" stroke="url(#maleGradC4)" stroke-width="13" stroke-linecap="round"/>
  <!-- Arms reaching forward toward toes -->
  <path d="M 84 94 L 142 126" stroke="url(#maleGradC4)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 5. Standing Quad Stretch
svg_c5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC5)"/>
  
  <!-- Balance Support Wall / Post on left -->
  <line x1="36" y1="35" x2="36" y2="175" stroke="#90caf9" stroke-width="4" stroke-linecap="round"/>

  <!-- Stretch tension highlight on front of thigh -->
  <path d="M 112 115 Q 120 135 116 148" fill="none" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>

  <!-- Male Athletic Figure Standing Upright -->
  <!-- Hand on wall for support -->
  <line x1="36" y1="84" x2="74" y2="84" stroke="url(#maleGradC5)" stroke-width="7" stroke-linecap="round"/>
  <!-- Head -->
  <circle cx="88" cy="46" r="14" fill="url(#maleGradC5)"/>
  <!-- Torso tall and upright -->
  <path d="M 88 58 L 88 114" stroke="url(#maleGradC5)" stroke-width="13" stroke-linecap="round"/>
  <!-- Standing Support Leg straight -->
  <path d="M 86 114 L 86 168" stroke="url(#maleGradC5)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 86 168 L 74 172" stroke="url(#maleGradC5)" stroke-width="7" stroke-linecap="round"/>
  
  <!-- Bent Quad Leg: Knee down, heel to glute -->
  <path d="M 90 114 L 110 148 L 114 104" fill="none" stroke="#1e88e5" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Right Arm reaching behind holding ankle -->
  <path d="M 90 74 L 114 88 L 114 104" fill="none" stroke="url(#maleGradC5)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Floor line -->
  <line x1="45" y1="172" x2="145" y2="172" stroke="#90caf9" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

# 6. Calm Recovery Walk
svg_c6 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradC6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradC6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#bgGradC6)"/>
  
  <!-- Calm Breath Wave Indicator at top -->
  <path d="M 120 38 Q 135 28 150 38 T 180 38" fill="none" stroke="#00acc1" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Male Athletic Figure in Relaxed Recovery Walk -->
  <!-- Head upright and relaxed -->
  <circle cx="104" cy="46" r="14" fill="url(#maleGradC6)"/>
  <!-- Torso relaxed upright -->
  <path d="M 104 58 L 102 112" stroke="url(#maleGradC6)" stroke-width="13" stroke-linecap="round"/>
  <!-- Arms swaying gently at sides -->
  <path d="M 102 72 L 90 98" stroke="url(#maleGradC6)" stroke-width="7" stroke-linecap="round"/>
  <path d="M 104 72 L 118 96" stroke="#1e88e5" stroke-width="7" stroke-linecap="round"/>
  
  <!-- Legs in gentle walking stride -->
  <path d="M 102 112 L 86 166" stroke="url(#maleGradC6)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 86 166 L 76 170" stroke="url(#maleGradC6)" stroke-width="7" stroke-linecap="round"/>
  <path d="M 102 112 L 122 164" stroke="#1e88e5" stroke-width="10" stroke-linecap="round"/>
  <path d="M 122 164 L 134 168" stroke="#1e88e5" stroke-width="7" stroke-linecap="round"/>

  <!-- Ground Line -->
  <line x1="40" y1="170" x2="160" y2="170" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>
</svg>"""

# Save Warmup SVGs
warmups = [
    ("warmup-01-cardio.svg", svg_w1),
    ("warmup-02-arm-circles.svg", svg_w2),
    ("warmup-03-leg-swings.svg", svg_w3),
    ("warmup-04-hip-circles.svg", svg_w4),
    ("warmup-05-bodyweight-squat.svg", svg_w5),
    ("warmup-06-warmup-set.svg", svg_w6),
]

for filename, content in warmups:
    path = os.path.join(warmup_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {path} ({os.path.getsize(path):,} bytes)")

# Save Cooldown SVGs
cooldowns = [
    ("cooldown-01-shoulder-stretch.svg", svg_c1),
    ("cooldown-02-chest-stretch.svg", svg_c2),
    ("cooldown-03-lower-back-stretch.svg", svg_c3),
    ("cooldown-04-hamstring-stretch.svg", svg_c4),
    ("cooldown-05-quad-stretch.svg", svg_c5),
    ("cooldown-06-calm-walk.svg", svg_c6),
]

for filename, content in cooldowns:
    path = os.path.join(cooldown_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {path} ({os.path.getsize(path):,} bytes)")
