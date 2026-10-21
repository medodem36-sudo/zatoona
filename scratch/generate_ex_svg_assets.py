# -*- coding: utf-8 -*-
import os

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
ex_dir = os.path.join(repo, "assets", "images", "exercises")
os.makedirs(ex_dir, exist_ok=True)

# ── ROUTINE A ──

# 1. Goblet Squat
svg_a1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA1)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="102" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="69" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">GOBLET SQUAT</text>

  <!-- Motion arrows -->
  <path d="M 68 85 L 68 125" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="68,132 62,122 74,122" fill="#e65100"/>
  <polygon points="68,78 62,88 74,88" fill="#e65100"/>

  <!-- Male Athletic Figure in Deep Goblet Squat -->
  <!-- Head -->
  <circle cx="155" cy="52" r="15" fill="url(#maleGradA1)"/>
  <!-- Torso (athletic flat back angled forward 45°) -->
  <path d="M 152 66 L 122 115" stroke="url(#maleGradA1)" stroke-width="15" stroke-linecap="round"/>
  
  <!-- Arms holding Dumbbell vertically at sternum -->
  <path d="M 148 76 L 174 88 L 168 96" fill="none" stroke="url(#maleGradA1)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Vertical Dumbbell -->
  <rect x="164" y="74" width="16" height="32" rx="3" fill="#37474f"/>
  <rect x="160" y="72" width="24" height="7" rx="2" fill="#78909c"/>
  <rect x="160" y="101" width="24" height="7" rx="2" fill="#78909c"/>

  <!-- Thigh (parallel to floor) -->
  <path d="M 122 115 L 178 116" stroke="url(#maleGradA1)" stroke-width="14" stroke-linecap="round"/>
  <!-- Shin (45° forward angle) -->
  <path d="M 178 116 L 164 170" stroke="url(#maleGradA1)" stroke-width="11" stroke-linecap="round"/>
  <!-- Foot flat on ground -->
  <path d="M 156 170 L 186 170" stroke="url(#maleGradA1)" stroke-width="9" stroke-linecap="round"/>

  <!-- Highlight Quadriceps/Glutes -->
  <path d="M 132 112 L 168 113" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
</svg>"""

# 2. Bench Press
svg_a2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA2)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="94" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="65" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">BENCH PRESS</text>

  <!-- Workout Bench -->
  <rect x="70" y="124" width="120" height="12" rx="3" fill="#263238"/>
  <!-- Bench Legs -->
  <rect x="80" y="136" width="10" height="36" fill="#455a64"/>
  <rect x="170" y="136" width="10" height="36" fill="#455a64"/>

  <!-- Press vertical motion arrow -->
  <path d="M 125 50 L 125 80" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="125,44 119,54 131,54" fill="#e65100"/>

  <!-- Male Athletic Figure Lying on Bench -->
  <!-- Head on bench -->
  <circle cx="82" cy="116" r="14" fill="url(#maleGradA2)"/>
  <!-- Torso resting on bench -->
  <path d="M 94 122 L 152 122" stroke="url(#maleGradA2)" stroke-width="14" stroke-linecap="round"/>
  <!-- Legs bent with feet flat on ground -->
  <path d="M 152 122 L 180 134 L 186 172" fill="none" stroke="url(#maleGradA2)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 186 172 L 202 172" stroke="url(#maleGradA2)" stroke-width="8" stroke-linecap="round"/>

  <!-- Arms pressing Barbell upward -->
  <path d="M 116 118 L 124 88 L 124 58" fill="none" stroke="url(#maleGradA2)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Barbell and Weight Plates -->
  <line x1="50" y1="58" x2="200" y2="58" stroke="#37474f" stroke-width="5" stroke-linecap="round"/>
  <!-- Left Weight Plate -->
  <rect x="62" y="42" width="10" height="32" rx="2" fill="#78909c"/>
  <rect x="56" y="46" width="6" height="24" rx="2" fill="#90a4ae"/>
  <!-- Right Weight Plate -->
  <rect x="180" y="42" width="10" height="32" rx="2" fill="#78909c"/>
  <rect x="190" y="46" width="6" height="24" rx="2" fill="#90a4ae"/>
  
  <!-- Chest muscle engagement highlight -->
  <circle cx="116" cy="118" r="6" fill="#e65100"/>
</svg>"""

# 3. Lat Pulldown
svg_a3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA3)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="100" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="68" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">LAT PULLDOWN</text>

  <!-- Pulley Machine Frame -->
  <rect x="146" y="18" width="8" height="42" fill="#455a64"/>
  <circle cx="150" cy="38" r="9" fill="#263238"/>
  <!-- Pulley Cable -->
  <line x1="150" y1="38" x2="150" y2="70" stroke="#37474f" stroke-width="2.5"/>
  <!-- Wide Lat Bar -->
  <path d="M 95 64 Q 150 72 205 64" fill="none" stroke="#263238" stroke-width="5" stroke-linecap="round"/>

  <!-- Downward pull arrows -->
  <path d="M 85 75 L 85 95 M 215 75 L 215 95" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="85,100 80,91 90,91" fill="#e65100"/>
  <polygon points="215,100 210,91 220,91" fill="#e65100"/>

  <!-- Machine Seat & Thigh Pad -->
  <rect x="120" y="128" width="55" height="10" rx="2" fill="#263238"/>
  <rect x="142" y="138" width="10" height="34" fill="#455a64"/>
  <rect x="160" y="112" width="18" height="8" rx="2" fill="#455a64"/>

  <!-- Male Athletic Figure Seated Pulling Bar Down -->
  <!-- Head slightly tilted back -->
  <circle cx="150" cy="78" r="14" fill="url(#maleGradA3)"/>
  <!-- Torso (lean slightly back 15°) -->
  <path d="M 150 92 L 144 134" stroke="url(#maleGradA3)" stroke-width="15" stroke-linecap="round"/>
  <!-- Broad Lats highlighted -->
  <path d="M 136 102 Q 150 108 164 102" stroke="#e65100" stroke-width="4" stroke-linecap="round"/>
  
  <!-- Arms pulling wide bar -->
  <path d="M 144 94 L 115 82 L 102 66" fill="none" stroke="url(#maleGradA3)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 154 94 L 185 82 L 198 66" fill="none" stroke="url(#maleGradA3)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Thighs anchored under pad -->
  <path d="M 144 134 L 176 130 L 174 172" fill="none" stroke="url(#maleGradA3)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 174 172 L 190 172" stroke="url(#maleGradA3)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 4. Overhead Shoulder Press
svg_a4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA4)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="112" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="74" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">OVERHEAD PRESS</text>

  <!-- Upward press motion arrows -->
  <path d="M 98 75 L 98 48 M 202 75 L 202 48" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="98,42 93,52 103,52" fill="#e65100"/>
  <polygon points="202,42 197,52 207,52" fill="#e65100"/>

  <!-- Male Athletic Figure Pressing Dumbbells Overhead -->
  <!-- Head -->
  <circle cx="150" cy="56" r="14" fill="url(#maleGradA4)"/>
  <!-- Broad Torso -->
  <path d="M 126 84 Q 150 78 174 84 L 164 130 L 136 130 Z" fill="url(#maleGradA4)"/>
  
  <!-- Deltoid highlight -->
  <circle cx="126" cy="85" r="5" fill="#e65100"/>
  <circle cx="174" cy="85" r="5" fill="#e65100"/>

  <!-- Left Arm pressed overhead -->
  <path d="M 130 84 L 112 65 L 112 38" fill="none" stroke="url(#maleGradA4)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Left Dumbbell -->
  <rect x="100" y="32" width="24" height="6" rx="2" fill="#37474f"/>
  <rect x="96" y="27" width="8" height="16" rx="2" fill="#78909c"/>
  <rect x="120" y="27" width="8" height="16" rx="2" fill="#78909c"/>

  <!-- Right Arm pressed overhead -->
  <path d="M 170 84 L 188 65 L 188 38" fill="none" stroke="url(#maleGradA4)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Right Dumbbell -->
  <rect x="176" y="32" width="24" height="6" rx="2" fill="#37474f"/>
  <rect x="172" y="27" width="8" height="16" rx="2" fill="#78909c"/>
  <rect x="196" y="27" width="8" height="16" rx="2" fill="#78909c"/>

  <!-- Legs solid upright shoulder-width stance -->
  <path d="M 140 130 L 134 172" stroke="url(#maleGradA4)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 160 130 L 166 172" stroke="url(#maleGradA4)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 134 172 L 122 172 M 166 172 L 178 172" stroke="url(#maleGradA4)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 5. Core Plank
svg_a5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA5)"/>
  
  <!-- Exercise Mat on Floor -->
  <rect x="35" y="162" width="230" height="10" rx="4" fill="#a5d6a7" stroke="#81c784" stroke-width="1.5"/>

  <!-- Badge -->
  <rect x="18" y="16" width="86" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="61" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">CORE PLANK</text>

  <!-- Straight alignment reference line -->
  <line x1="70" y1="112" x2="235" y2="152" stroke="#e65100" stroke-width="2" stroke-dasharray="6 4"/>

  <!-- Core stability ring -->
  <ellipse cx="140" cy="130" rx="14" ry="8" fill="none" stroke="#e65100" stroke-width="2.5"/>

  <!-- Male Athletic Figure in Rigid Forearm Plank -->
  <!-- Head aligned with spine -->
  <circle cx="68" cy="108" r="14" fill="url(#maleGradA5)"/>
  <!-- Rigid Torso -->
  <path d="M 80 115 L 150 132" stroke="url(#maleGradA5)" stroke-width="15" stroke-linecap="round"/>
  <!-- Forearm on mat (elbow at 90°) -->
  <path d="M 86 118 L 86 162 L 108 162" fill="none" stroke="url(#maleGradA5)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Legs in straight extension -->
  <path d="M 150 132 L 230 152" stroke="url(#maleGradA5)" stroke-width="12" stroke-linecap="round"/>
  <!-- Toes tucked on mat -->
  <path d="M 230 152 L 234 162" stroke="url(#maleGradA5)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 6. Face Pull
svg_a6 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExA6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2f7ec"/>
    </linearGradient>
    <linearGradient id="maleGradA6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b5e20"/>
      <stop offset="100%" stop-color="#0a3310"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExA6)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#a5d6a7" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="86" height="22" rx="6" fill="#e8f5e9" stroke="#81c784" stroke-width="1.2"/>
  <text x="61" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1b5e20" text-anchor="middle">FACE PULL</text>

  <!-- High Cable Pulley Post on Left -->
  <rect x="36" y="30" width="10" height="142" rx="2" fill="#455a64"/>
  <circle cx="41" cy="74" r="8" fill="#263238"/>
  
  <!-- Cable taut to face height -->
  <line x1="41" y1="74" x2="132" y2="76" stroke="#37474f" stroke-width="2.5"/>
  <!-- Rope Attachment split -->
  <path d="M 132 76 L 146 64 M 132 76 L 146 88" stroke="#78909c" stroke-width="4" stroke-linecap="round"/>

  <!-- High Elbow Pull Arrows -->
  <path d="M 138 60 Q 152 54 165 60" fill="none" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="168,63 158,58 162,68" fill="#e65100"/>

  <!-- Male Athletic Figure Standing Pulling to Eyes -->
  <!-- Head -->
  <circle cx="170" cy="54" r="14" fill="url(#maleGradA4)"/>
  <!-- Torso leaned slightly back for balance -->
  <path d="M 170 68 L 180 124" stroke="url(#maleGradA6)" stroke-width="14" stroke-linecap="round"/>
  <!-- Rear Delts / Upper Back highlight -->
  <circle cx="180" cy="74" r="6" fill="#e65100"/>
  
  <!-- High flaring elbows pulling rope to face -->
  <path d="M 174 72 L 188 64 L 146 64" fill="none" stroke="url(#maleGradA6)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 174 74 L 186 86 L 146 88" fill="none" stroke="url(#maleGradA6)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Staggered athletic stance -->
  <path d="M 180 124 L 166 172" stroke="url(#maleGradA6)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 180 124 L 204 172" stroke="url(#maleGradA6)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 166 172 L 154 172 M 204 172 L 216 172" stroke="url(#maleGradA6)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# ── ROUTINE B ──

# 1. Romanian Deadlift (RDL)
svg_b1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB1)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="124" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="80" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">ROMANIAN DEADLIFT</text>

  <!-- Hip hinge back arrow -->
  <path d="M 165 92 Q 190 95 198 108" fill="none" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="202,112 192,106 196,116" fill="#e65100"/>

  <!-- Male Athletic Figure in Hip Hinge Position -->
  <!-- Head in neutral alignment with spine -->
  <circle cx="106" cy="74" r="14" fill="url(#maleGradB1)"/>
  <!-- Torso (flat back hinged forward to ~45°) -->
  <path d="M 116 82 L 176 108" stroke="url(#maleGradB1)" stroke-width="14" stroke-linecap="round"/>
  
  <!-- Hamstrings & Glutes Highlight -->
  <path d="M 176 108 L 158 140" stroke="#e65100" stroke-width="4" stroke-linecap="round"/>
  
  <!-- Arms hanging vertically holding Barbell close to shins -->
  <line x1="124" y1="88" x2="134" y2="138" stroke="url(#maleGradB1)" stroke-width="9" stroke-linecap="round"/>
  <!-- Barbell -->
  <line x1="105" y1="138" x2="165" y2="138" stroke="#37474f" stroke-width="5" stroke-linecap="round"/>
  <circle cx="108" cy="138" r="14" fill="#546e7a"/>
  <circle cx="162" cy="138" r="14" fill="#546e7a"/>

  <!-- Legs: soft knee bend, shins nearly vertical -->
  <path d="M 176 108 L 160 142 L 154 172" fill="none" stroke="url(#maleGradB1)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 154 172 L 140 172" stroke="url(#maleGradB1)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 2. Barbell Bent-over Row
svg_b2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB2)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="94" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="65" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">BARBELL ROW</text>

  <!-- Upward row pull motion arrow -->
  <path d="M 134 140 L 140 108" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="142,102 134,110 145,112" fill="#e65100"/>

  <!-- Male Athletic Figure in Bent-over Row -->
  <!-- Head neutral -->
  <circle cx="112" cy="74" r="14" fill="url(#maleGradB2)"/>
  <!-- Torso (flat back at 45°) -->
  <path d="M 122 82 L 180 112" stroke="url(#maleGradB2)" stroke-width="14" stroke-linecap="round"/>
  
  <!-- Back / Lat engagement highlight -->
  <circle cx="148" cy="94" r="6" fill="#e65100"/>

  <!-- Arm pulling barbell up toward lower chest/ribs -->
  <path d="M 132 88 L 158 92 L 144 114" fill="none" stroke="url(#maleGradB2)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Barbell pulled close to abdomen -->
  <line x1="110" y1="114" x2="175" y2="114" stroke="#37474f" stroke-width="5" stroke-linecap="round"/>
  <rect x="112" y="98" width="8" height="32" rx="2" fill="#546e7a"/>
  <rect x="165" y="98" width="8" height="32" rx="2" fill="#546e7a"/>

  <!-- Legs with slight knee bend -->
  <path d="M 180 112 L 166 142 L 160 172" fill="none" stroke="url(#maleGradB2)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 160 172 L 146 172" stroke="url(#maleGradB2)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 3. Push-ups
svg_b3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB3)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="76" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="56" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">PUSH-UPS</text>

  <!-- Push up motion arrow -->
  <path d="M 100 105 L 100 135" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="100,98 94,108 106,108" fill="#e65100"/>
  <polygon points="100,142 94,132 106,132" fill="#e65100"/>

  <!-- Male Athletic Figure in Mid-phase Push-up -->
  <!-- Head -->
  <circle cx="78" cy="116" r="14" fill="url(#maleGradB3)"/>
  <!-- Torso & Hips straight line -->
  <path d="M 90 125 L 170 142" stroke="url(#maleGradB3)" stroke-width="14" stroke-linecap="round"/>
  <!-- Pectoral / Tricep engagement highlight -->
  <circle cx="105" cy="130" r="5" fill="#e65100"/>

  <!-- Arm bent at 90° pushing off floor -->
  <path d="M 104 128 L 104 150 L 118 172" fill="none" stroke="url(#maleGradB3)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Palm on floor -->
  <path d="M 112 172 L 126 172" stroke="url(#maleGradB3)" stroke-width="7" stroke-linecap="round"/>

  <!-- Legs extended -->
  <path d="M 170 142 L 240 158" stroke="url(#maleGradB3)" stroke-width="11" stroke-linecap="round"/>
  <!-- Toes anchored on floor -->
  <path d="M 240 158 L 244 172" stroke="url(#maleGradB3)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 4. Pull-ups
svg_b4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB4)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="76" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="56" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">PULL-UPS</text>

  <!-- Pull-up Rig & Bar at Top -->
  <line x1="60" y1="36" x2="240" y2="36" stroke="#263238" stroke-width="5" stroke-linecap="round"/>
  <rect x="75" y="24" width="8" height="20" fill="#455a64"/>
  <rect x="215" y="24" width="8" height="20" fill="#455a64"/>

  <!-- Upward pull motion arrows -->
  <path d="M 120 75 L 120 52 M 180 75 L 180 52" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="120,46 115,56 125,56" fill="#e65100"/>
  <polygon points="180,46 175,56 185,56" fill="#e65100"/>

  <!-- Male Athletic Figure at Top of Pull-up (Chin over bar) -->
  <!-- Head clearing bar -->
  <circle cx="150" cy="30" r="14" fill="url(#maleGradB4)"/>
  <!-- Torso -->
  <path d="M 132 50 Q 150 44 168 50 L 160 98 L 140 98 Z" fill="url(#maleGradB4)"/>
  
  <!-- Latissimus dorsi & Bicep highlight -->
  <path d="M 132 52 Q 150 58 168 52" stroke="#e65100" stroke-width="4" stroke-linecap="round"/>

  <!-- Arms flexed pulling body up -->
  <path d="M 134 50 L 118 42 L 122 36" fill="none" stroke="url(#maleGradB4)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 166 50 L 182 42 L 178 36" fill="none" stroke="url(#maleGradB4)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Hanging Legs slightly crossed at ankles -->
  <path d="M 145 98 L 144 150 L 150 165" fill="none" stroke="url(#maleGradB4)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 155 98 L 156 148 L 150 165" fill="none" stroke="url(#maleGradB4)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# 5. Abdominal Crunch
svg_b5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB5)"/>
  
  <!-- Exercise Mat on Floor -->
  <rect x="35" y="162" width="230" height="10" rx="4" fill="#bbdefb" stroke="#90caf9" stroke-width="1.5"/>

  <!-- Badge -->
  <rect x="18" y="16" width="76" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="56" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">CRUNCH</text>

  <!-- Abdominal contraction arc arrow -->
  <path d="M 95 105 Q 118 90 142 108" fill="none" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="90,108 100,104 98,114" fill="#e65100"/>

  <!-- Male Athletic Figure Performing Crunch -->
  <!-- Upper Back & Shoulders curled 30° off floor -->
  <!-- Head -->
  <circle cx="82" cy="118" r="14" fill="url(#maleGradB5)"/>
  <!-- Hands lightly supporting back of head -->
  <path d="M 98 132 L 80 128 L 74 120" fill="none" stroke="url(#maleGradB5)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Curled upper torso -->
  <path d="M 92 130 L 126 148 L 158 152" fill="none" stroke="url(#maleGradB5)" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Core contraction highlight -->
  <circle cx="128" cy="142" r="6" fill="#e65100"/>

  <!-- Knees bent at 90°, feet flat on floor -->
  <path d="M 158 152 L 188 116 L 218 162" fill="none" stroke="url(#maleGradB5)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 218 162 L 232 162" stroke="url(#maleGradB5)" stroke-width="8" stroke-linecap="round"/>
</svg>"""

# 6. Lunges
svg_b6 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgExB6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f7ff"/>
      <stop offset="100%" stop-color="#e3f0fd"/>
    </linearGradient>
    <linearGradient id="maleGradB6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d47a1"/>
      <stop offset="100%" stop-color="#1565c0"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgExB6)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="172" x2="275" y2="172" stroke="#90caf9" stroke-width="3" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="16" width="76" height="22" rx="6" fill="#e3f2fd" stroke="#90caf9" stroke-width="1.2"/>
  <text x="56" y="31" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="9" font-weight="bold" fill="#0d47a1" text-anchor="middle">LUNGES</text>

  <!-- Down/Up lunge motion arrows -->
  <path d="M 72 90 L 72 130" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="72,136 66,126 78,126" fill="#e65100"/>
  <polygon points="72,84 66,94 78,94" fill="#e65100"/>

  <!-- Male Athletic Figure in Lunge Position -->
  <!-- Head upright -->
  <circle cx="152" cy="48" r="14" fill="url(#maleGradB6)"/>
  <!-- Torso perfectly upright -->
  <path d="M 152 62 L 152 118" stroke="url(#maleGradB6)" stroke-width="14" stroke-linecap="round"/>
  <!-- Hands on hips or holding light dumbbells -->
  <path d="M 150 74 L 136 94 L 148 106" fill="none" stroke="url(#maleGradB6)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  
  <!-- Quadriceps/Glute highlight -->
  <circle cx="170" cy="120" r="5" fill="#e65100"/>

  <!-- Front Leg: thigh parallel to floor, knee at 90° over ankle -->
  <path d="M 152 118 L 188 120 L 186 172" fill="none" stroke="url(#maleGradB6)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 186 172 L 202 172" stroke="url(#maleGradB6)" stroke-width="8" stroke-linecap="round"/>

  <!-- Rear Leg: knee hovering just above floor at 90° -->
  <path d="M 152 118 L 126 138 L 122 166" fill="none" stroke="url(#maleGradB6)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Rear toes flexed on floor -->
  <path d="M 122 166 L 110 172" stroke="url(#maleGradB6)" stroke-width="7" stroke-linecap="round"/>
</svg>"""

exercises = [
    ("ex-a01-goblet-squat.svg", svg_a1),
    ("ex-a02-bench-press.svg", svg_a2),
    ("ex-a03-lat-pulldown.svg", svg_a3),
    ("ex-a04-overhead-press.svg", svg_a4),
    ("ex-a05-plank.svg", svg_a5),
    ("ex-a06-face-pull.svg", svg_a6),
    ("ex-b01-romanian-deadlift.svg", svg_b1),
    ("ex-b02-barbell-row.svg", svg_b2),
    ("ex-b03-push-up.svg", svg_b3),
    ("ex-b04-pull-up.svg", svg_b4),
    ("ex-b05-abdominal-crunch.svg", svg_b5),
    ("ex-b06-lunges.svg", svg_b6),
]

for filename, content in exercises:
    path = os.path.join(ex_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {path} ({os.path.getsize(path):,} bytes)")
