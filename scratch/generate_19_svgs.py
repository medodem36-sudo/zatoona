import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

SVG_DIR = 'assets/images/exercises'
os.makedirs(SVG_DIR, exist_ok=True)

# 1. Barbell Back Squat
svg_back_squat = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgBackSquat" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf4ff"/>
      <stop offset="100%" stop-color="#fae8ff"/>
    </linearGradient>
    <linearGradient id="maleGradSquat" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4a044e"/>
      <stop offset="100%" stop-color="#701a75"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgBackSquat)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#e879f9" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="130" height="22" rx="6" fill="#fdf2f8" stroke="#f472b6" stroke-width="1.2"/>
  <text x="83" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#831843" text-anchor="middle">BARBELL BACK SQUAT</text>

  <!-- Motion arrows -->
  <path d="M 62 82 L 62 128" stroke="#e65100" stroke-width="2.2" stroke-linecap="round"/>
  <polygon points="62,135 57,125 67,125" fill="#e65100"/>
  <polygon points="62,75 57,85 67,85" fill="#e65100"/>

  <!-- Squat Rack Uprights (background) -->
  <line x1="105" y1="45" x2="105" y2="175" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>
  <line x1="225" y1="45" x2="225" y2="175" stroke="#cbd5e1" stroke-width="3" stroke-linecap="round"/>
  <line x1="100" y1="85" x2="110" y2="85" stroke="#94a3b8" stroke-width="3"/>
  <line x1="220" y1="85" x2="230" y2="85" stroke="#94a3b8" stroke-width="3"/>

  <!-- Athletic Male Figure in Parallel Back Squat (Side View angled) -->
  <!-- Head & Neck -->
  <circle cx="174" cy="56" r="14" fill="url(#maleGradSquat)"/>
  
  <!-- Torso (flat back, ~45 deg forward incline) -->
  <path d="M 166 68 L 132 118" stroke="url(#maleGradSquat)" stroke-width="15" stroke-linecap="round"/>
  
  <!-- Arms & Hands gripping Barbell on upper traps -->
  <path d="M 160 76 L 152 70 L 160 66" fill="none" stroke="url(#maleGradSquat)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Barbell resting on Upper Traps -->
  <line x1="85" y1="67" x2="245" y2="67" stroke="#64748b" stroke-width="5" stroke-linecap="round"/>
  <!-- Plates (Standard 45lb/20kg Olympic Plates) -->
  <rect x="88" y="45" width="10" height="44" rx="2" fill="#1e293b"/>
  <rect x="80" y="49" width="7" height="36" rx="2" fill="#334155"/>
  <rect x="232" y="45" width="10" height="44" rx="2" fill="#1e293b"/>
  <rect x="243" y="49" width="7" height="36" rx="2" fill="#334155"/>

  <!-- Thigh (parallel to ground at 90 deg hip angle) -->
  <path d="M 132 118 L 188 120" stroke="url(#maleGradSquat)" stroke-width="14" stroke-linecap="round"/>
  <!-- Shin (angled forward over toes) -->
  <path d="M 188 120 L 176 173" stroke="url(#maleGradSquat)" stroke-width="11" stroke-linecap="round"/>
  <!-- Foot (flat on ground) -->
  <path d="M 166 174 L 198 174" stroke="url(#maleGradSquat)" stroke-width="8" stroke-linecap="round"/>

  <!-- Highlight Quadriceps & Glute contraction -->
  <path d="M 142 116 L 178 117" stroke="#e65100" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="134" cy="118" r="4.5" fill="#e65100"/>
</svg>"""

# 2. Conventional Deadlift
svg_deadlift = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgDeadlift" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="maleGradDeadlift" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgDeadlift)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="144" height="22" rx="6" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="90" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#0f172a" text-anchor="middle">CONVENTIONAL DEADLIFT</text>

  <!-- Motion upward arrow -->
  <path d="M 60 135 L 60 85" stroke="#e65100" stroke-width="2.2" stroke-linecap="round"/>
  <polygon points="60,78 55,88 65,88" fill="#e65100"/>

  <!-- Male Athletic Figure in Deadlift Pull (Mid-Shin hinge) -->
  <!-- Head & Gaze forward-down -->
  <circle cx="188" cy="68" r="14" fill="url(#maleGradDeadlift)"/>
  
  <!-- Torso (rigid flat back, 35 deg angle) -->
  <path d="M 180 78 L 132 116" stroke="url(#maleGradDeadlift)" stroke-width="14" stroke-linecap="round"/>

  <!-- Thighs (Hips hinged back, knees semi-flexed) -->
  <path d="M 132 116 L 166 142" stroke="url(#maleGradDeadlift)" stroke-width="13" stroke-linecap="round"/>
  <!-- Shins (nearly vertical) -->
  <path d="M 166 142 L 160 174" stroke="url(#maleGradDeadlift)" stroke-width="10" stroke-linecap="round"/>
  <!-- Feet -->
  <path d="M 150 174 L 180 174" stroke="url(#maleGradDeadlift)" stroke-width="8" stroke-linecap="round"/>

  <!-- Arms (hanging perfectly straight down from shoulders) -->
  <path d="M 176 84 L 176 138" stroke="url(#maleGradDeadlift)" stroke-width="8" stroke-linecap="round"/>

  <!-- Barbell at Mid-Shin (close to shins) -->
  <line x1="100" y1="140" x2="250" y2="140" stroke="#64748b" stroke-width="5" stroke-linecap="round"/>
  <!-- Olympic Plates touching / near floor -->
  <rect x="105" y="118" width="10" height="44" rx="2" fill="#020617"/>
  <rect x="97" y="122" width="7" height="36" rx="2" fill="#1e293b"/>
  <rect x="235" y="118" width="10" height="44" rx="2" fill="#020617"/>
  <rect x="246" y="122" width="7" height="36" rx="2" fill="#1e293b"/>

  <!-- Posterior Chain Activation Line (Glutes/Hamstrings/Erectors) -->
  <path d="M 176 80 L 134 116 L 164 140" fill="none" stroke="#e65100" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

# 3. Incline Barbell Bench Press
svg_incline_barbell = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgIncBB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eff6ff"/>
      <stop offset="100%" stop-color="#dbeafe"/>
    </linearGradient>
    <linearGradient id="maleGradIncBB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e3a8a"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgIncBB)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#93c5fd" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="154" height="22" rx="6" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.2"/>
  <text x="95" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">INCLINE BARBELL BENCH PRESS</text>

  <!-- Incline Bench (35-40 deg) -->
  <!-- Frame & Base -->
  <line x1="90" y1="174" x2="160" y2="174" stroke="#475569" stroke-width="4" stroke-linecap="round"/>
  <line x1="110" y1="174" x2="128" y2="118" stroke="#475569" stroke-width="5"/>
  <line x1="150" y1="174" x2="150" y2="135" stroke="#475569" stroke-width="4"/>
  <!-- Incline Backrest Pad -->
  <line x1="102" y1="84" x2="148" y2="142" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>
  <!-- Seat Pad -->
  <line x1="144" y1="144" x2="168" y2="138" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>

  <!-- Bench Rack Posts behind lifter -->
  <line x1="88" y1="52" x2="88" y2="174" stroke="#64748b" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="84" y1="78" x2="94" y2="78" stroke="#94a3b8" stroke-width="3"/>

  <!-- Athletic Male Figure on Incline Bench -->
  <!-- Head on upper pad -->
  <circle cx="114" cy="74" r="13" fill="url(#maleGradIncBB)"/>
  <!-- Torso along incline pad -->
  <path d="M 122 84 L 148 138" stroke="url(#maleGradIncBB)" stroke-width="14" stroke-linecap="round"/>
  <!-- Thigh & Leg down to floor -->
  <path d="M 148 138 L 180 148 L 184 174" fill="none" stroke="url(#maleGradIncBB)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Arms pressing Barbell vertically above upper chest -->
  <path d="M 132 94 L 148 72 L 150 56" fill="none" stroke="url(#maleGradIncBB)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Barbell across Upper Chest (pressing path) -->
  <line x1="105" y1="54" x2="205" y2="54" stroke="#64748b" stroke-width="4.5" stroke-linecap="round"/>
  <!-- Plates -->
  <rect x="108" y="38" width="8" height="32" rx="2" fill="#0f172a"/>
  <rect x="195" y="38" width="8" height="32" rx="2" fill="#0f172a"/>

  <!-- Upper Chest engagement highlight -->
  <circle cx="136" cy="94" r="5" fill="#e65100"/>
  <!-- Push direction arrow -->
  <path d="M 160 76 L 168 56" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="171,51 163,57 172,61" fill="#e65100"/>
</svg>"""

# 4. Incline Dumbbell Press
svg_incline_dumbbell = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgIncDB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdfa"/>
      <stop offset="100%" stop-color="#ccfbf1"/>
    </linearGradient>
    <linearGradient id="maleGradIncDB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#115e59"/>
      <stop offset="100%" stop-color="#042f2e"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgIncDB)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#5eead4" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="156" height="22" rx="6" fill="#f0fdfa" stroke="#2dd4bf" stroke-width="1.2"/>
  <text x="96" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#115e59" text-anchor="middle">INCLINE DUMBBELL PRESS</text>

  <!-- Incline Bench (35-40 deg) -->
  <line x1="90" y1="174" x2="160" y2="174" stroke="#475569" stroke-width="4" stroke-linecap="round"/>
  <line x1="112" y1="174" x2="128" y2="118" stroke="#475569" stroke-width="5"/>
  <line x1="152" y1="174" x2="152" y2="135" stroke="#475569" stroke-width="4"/>
  <!-- Incline Backrest Pad -->
  <line x1="102" y1="84" x2="148" y2="142" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>
  <!-- Seat Pad -->
  <line x1="144" y1="144" x2="168" y2="138" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>

  <!-- Athletic Male Figure on Incline Bench -->
  <circle cx="114" cy="74" r="13" fill="url(#maleGradIncDB)"/>
  <path d="M 122 84 L 148 138" stroke="url(#maleGradIncDB)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 148 138 L 180 148 L 184 174" fill="none" stroke="url(#maleGradIncDB)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Left Arm (pressed up with Dumbbell) -->
  <path d="M 130 92 L 142 66 L 144 52" fill="none" stroke="url(#maleGradIncDB)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Dumbbell 1 (hex plates) -->
  <rect x="135" y="44" width="18" height="6" rx="2" fill="#334155"/>
  <rect x="131" y="38" width="6" height="18" rx="2" fill="#0f172a"/>
  <rect x="151" y="38" width="6" height="18" rx="2" fill="#0f172a"/>

  <!-- Right Arm (parallel pressing with second dumbbell) -->
  <path d="M 136 96 L 160 70 L 166 58" fill="none" stroke="url(#maleGradIncDB)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Dumbbell 2 -->
  <rect x="158" y="50" width="16" height="5" rx="2" fill="#334155"/>
  <rect x="155" y="45" width="5" height="15" rx="2" fill="#0f172a"/>
  <rect x="171" y="45" width="5" height="15" rx="2" fill="#0f172a"/>

  <!-- Upper Chest engagement highlight -->
  <circle cx="134" cy="94" r="5" fill="#e65100"/>
  <path d="M 172 74 L 180 56" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="183,52 175,57 184,62" fill="#e65100"/>
</svg>"""

# 5. Dumbbell Bench Press (Flat)
svg_dumbbell_bench = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgDBBench" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff7ed"/>
      <stop offset="100%" stop-color="#ffedd5"/>
    </linearGradient>
    <linearGradient id="maleGradDBBench" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9a3412"/>
      <stop offset="100%" stop-color="#7c2d12"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgDBBench)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#fed7aa" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="146" height="22" rx="6" fill="#fff7ed" stroke="#fb923c" stroke-width="1.2"/>
  <text x="91" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#9a3412" text-anchor="middle">DUMBBELL BENCH PRESS</text>

  <!-- Flat Bench -->
  <line x1="75" y1="174" x2="75" y2="128" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="195" y1="174" x2="195" y2="128" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="60" y1="124" x2="205" y2="124" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>

  <!-- Male Lifter Lying Flat on Bench -->
  <!-- Head on left side of bench -->
  <circle cx="80" cy="112" r="13" fill="url(#maleGradDBBench)"/>
  <!-- Torso horizontal on bench pad -->
  <path d="M 94 116 L 165 116" stroke="url(#maleGradDBBench)" stroke-width="14" stroke-linecap="round"/>
  <!-- Hips & Legs bent with feet flat on ground -->
  <path d="M 165 116 L 195 124 L 202 174" fill="none" stroke="url(#maleGradDBBench)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 194 174 L 216 174" stroke="url(#maleGradDBBench)" stroke-width="7" stroke-linecap="round"/>

  <!-- Arms pressing pair of Dumbbells vertically over sternum -->
  <!-- Left Arm -->
  <path d="M 122 112 L 118 78 L 118 58" fill="none" stroke="url(#maleGradDBBench)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Dumbbell 1 -->
  <rect x="110" y="52" width="16" height="6" rx="2" fill="#475569"/>
  <rect x="105" y="44" width="6" height="22" rx="2" fill="#0f172a"/>
  <rect x="125" y="44" width="6" height="22" rx="2" fill="#0f172a"/>

  <!-- Right Arm -->
  <path d="M 136 112 L 140 78 L 140 58" fill="none" stroke="url(#maleGradDBBench)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Dumbbell 2 -->
  <rect x="132" y="52" width="16" height="6" rx="2" fill="#475569"/>
  <rect x="127" y="44" width="6" height="22" rx="2" fill="#0f172a"/>
  <rect x="147" y="44" width="6" height="22" rx="2" fill="#0f172a"/>

  <!-- Chest Engagement Highlight -->
  <circle cx="128" cy="112" r="5" fill="#e65100"/>
  <!-- Upward pressing motion arrow -->
  <path d="M 158 84 L 158 52" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="158,46 153,56 163,56" fill="#e65100"/>
</svg>"""

# 6. Seated Cable Row
svg_cable_row = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgCableRow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="maleGradRow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgCableRow)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="132" height="22" rx="6" fill="#f1f5f9" stroke="#64748b" stroke-width="1.2"/>
  <text x="84" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#0f172a" text-anchor="middle">SEATED CABLE ROW</text>

  <!-- Low Row Machine Frame on Right -->
  <rect x="235" y="60" width="28" height="114" rx="3" fill="#334155"/>
  <line x1="249" y1="65" x2="249" y2="170" stroke="#94a3b8" stroke-width="3"/>
  <!-- Pulley wheel & Cable -->
  <circle cx="230" cy="130" r="7" fill="#64748b"/>
  <line x1="230" y1="130" x2="162" y2="116" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="4,2"/>
  
  <!-- Footplate & Bench -->
  <line x1="198" y1="116" x2="204" y2="148" stroke="#475569" stroke-width="6" stroke-linecap="round"/>
  <rect x="68" y="142" width="75" height="10" rx="2" fill="#1e293b"/>
  <line x1="105" y1="152" x2="105" y2="174" stroke="#475569" stroke-width="5"/>

  <!-- Male Athletic Figure Seated Upright Rowing -->
  <!-- Head & Neck -->
  <circle cx="106" cy="68" r="13" fill="url(#maleGradRow)"/>
  <!-- Torso (slight back arch, vertical upright) -->
  <path d="M 110 80 L 114 140" stroke="url(#maleGradRow)" stroke-width="14" stroke-linecap="round"/>
  <!-- Legs extended with soft knee bend to footplate -->
  <path d="M 114 140 L 158 136 L 200 134" fill="none" stroke="url(#maleGradRow)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Arms pulling V-handle into lower abdomen -->
  <path d="M 118 92 L 140 106 L 160 115" fill="none" stroke="url(#maleGradRow)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- V-Handle Grip -->
  <polygon points="160,111 166,115 160,119" fill="#0f172a"/>

  <!-- Back/Lats activation line & arrow -->
  <path d="M 106 88 L 106 118" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <path d="M 148 94 L 126 94" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="121,94 130,89 130,99" fill="#e65100"/>
</svg>"""

# 7. Leg Press (45 Degree)
svg_leg_press = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgLegPress" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf2f8"/>
      <stop offset="100%" stop-color="#fce7f3"/>
    </linearGradient>
    <linearGradient id="maleGradLegPress" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#831843"/>
      <stop offset="100%" stop-color="#500724"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgLegPress)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#f472b6" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="144" height="22" rx="6" fill="#fdf2f8" stroke="#ec4899" stroke-width="1.2"/>
  <text x="90" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#831843" text-anchor="middle">45° LEG PRESS MACHINE</text>

  <!-- 45-Degree Machine Rails & Frame -->
  <line x1="120" y1="168" x2="240" y2="48" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
  <line x1="140" y1="174" x2="255" y2="58" stroke="#475569" stroke-width="4" stroke-linecap="round"/>
  <line x1="230" y1="174" x2="230" y2="70" stroke="#94a3b8" stroke-width="4"/>

  <!-- Reclined Machine Seat Pad -->
  <line x1="68" y1="118" x2="98" y2="152" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>
  <line x1="98" y1="154" x2="124" y2="148" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>

  <!-- Sliding Sled & Footplate (at 45 deg) -->
  <line x1="205" y1="70" x2="225" y2="90" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>
  <!-- Weight Horn with Plates -->
  <line x1="215" y1="80" x2="195" y2="60" stroke="#94a3b8" stroke-width="5"/>
  <rect x="188" y="52" width="18" height="8" rx="2" transform="rotate(45 197 56)" fill="#1e293b"/>

  <!-- Male Athletic Figure on Leg Press -->
  <!-- Head & Neck -->
  <circle cx="76" cy="112" r="13" fill="url(#maleGradLegPress)"/>
  <!-- Torso resting on reclined backrest -->
  <path d="M 86 122 L 108 148" stroke="url(#maleGradLegPress)" stroke-width="13" stroke-linecap="round"/>
  <!-- Arms holding safety side handles -->
  <path d="M 95 132 L 110 144" stroke="url(#maleGradLegPress)" stroke-width="6" stroke-linecap="round"/>

  <!-- Legs in deep 90 deg press position against sled plate -->
  <path d="M 108 148 L 155 116 L 208 82" fill="none" stroke="url(#maleGradLegPress)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Quads / Glutes activation highlight -->
  <path d="M 122 140 L 150 120" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <circle cx="210" cy="80" r="4" fill="#e65100"/>
  <!-- Push arrow along 45 deg rail -->
  <path d="M 175 112 L 195 92" stroke="#e65100" stroke-width="2.2" stroke-linecap="round"/>
  <polygon points="199,87 189,92 195,98" fill="#e65100"/>
</svg>"""

# 8. Seated Dumbbell Shoulder Press
svg_seated_db_press = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgSeatedDBPress" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f5f3ff"/>
      <stop offset="100%" stop-color="#ede9fe"/>
    </linearGradient>
    <linearGradient id="maleGradSeatedPress" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#5b21b6"/>
      <stop offset="100%" stop-color="#3b0764"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgSeatedDBPress)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#c4b5fd" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="168" height="22" rx="6" fill="#f5f3ff" stroke="#a78bfa" stroke-width="1.2"/>
  <text x="102" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#5b21b6" text-anchor="middle">SEATED DUMBBELL SHOULDER PRESS</text>

  <!-- 90-Degree Upright Bench -->
  <line x1="120" y1="80" x2="120" y2="148" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>
  <line x1="120" y1="148" x2="148" y2="148" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>
  <line x1="116" y1="174" x2="116" y2="120" stroke="#475569" stroke-width="4"/>
  <line x1="142" y1="174" x2="142" y2="148" stroke="#475569" stroke-width="4"/>

  <!-- Male Athletic Figure Seated Upright -->
  <circle cx="132" cy="74" r="13" fill="url(#maleGradSeatedPress)"/>
  <path d="M 132 86 L 132 144" stroke="url(#maleGradSeatedPress)" stroke-width="13" stroke-linecap="round"/>
  <!-- Thighs horizontal, shins vertical, feet flat -->
  <path d="M 132 144 L 168 144 L 172 174" fill="none" stroke="url(#maleGradSeatedPress)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 166 174 L 186 174" stroke="url(#maleGradSeatedPress)" stroke-width="7" stroke-linecap="round"/>

  <!-- Left Arm (pressed overhead) -->
  <path d="M 130 92 L 116 68 L 118 48" fill="none" stroke="url(#maleGradSeatedPress)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Left Dumbbell -->
  <rect x="110" y="44" width="16" height="5" rx="2" fill="#475569"/>
  <rect x="106" y="38" width="5" height="17" rx="2" fill="#0f172a"/>
  <rect x="125" y="38" width="5" height="17" rx="2" fill="#0f172a"/>

  <!-- Right Arm (pressed overhead) -->
  <path d="M 136 92 L 152 68 L 150 48" fill="none" stroke="url(#maleGradSeatedPress)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Right Dumbbell -->
  <rect x="142" y="44" width="16" height="5" rx="2" fill="#475569"/>
  <rect x="138" y="38" width="5" height="17" rx="2" fill="#0f172a"/>
  <rect x="157" y="38" width="5" height="17" rx="2" fill="#0f172a"/>

  <!-- Deltoid Engagement Highlight -->
  <circle cx="124" cy="94" r="4.5" fill="#e65100"/>
  <circle cx="140" cy="94" r="4.5" fill="#e65100"/>
  <!-- Motion arrows upward -->
  <path d="M 164 68 L 164 48" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="164,43 160,51 168,51" fill="#e65100"/>
</svg>"""

# 9. Hanging Leg Raise
svg_hanging_leg_raise = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgHangingLeg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ecfeff"/>
      <stop offset="100%" stop-color="#cffafe"/>
    </linearGradient>
    <linearGradient id="maleGradHanging" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#155e75"/>
      <stop offset="100%" stop-color="#083344"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgHangingLeg)"/>

  <!-- Badge -->
  <rect x="18" y="14" width="138" height="22" rx="6" fill="#ecfeff" stroke="#22d3ee" stroke-width="1.2"/>
  <text x="87" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#155e75" text-anchor="middle">HANGING LEG RAISE</text>

  <!-- Pull-Up Bar Frame -->
  <line x1="60" y1="36" x2="240" y2="36" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="65" y1="36" x2="65" y2="185" stroke="#94a3b8" stroke-width="4"/>
  <line x1="235" y1="36" x2="235" y2="185" stroke="#94a3b8" stroke-width="4"/>

  <!-- Athletic Male Figure in Full Hanging Leg Raise (90 deg L-Sit) -->
  <!-- Arms hanging straight down from bar -->
  <line x1="135" y1="38" x2="135" y2="72" stroke="url(#maleGradHanging)" stroke-width="7" stroke-linecap="round"/>
  <!-- Head positioned between arms -->
  <circle cx="135" cy="62" r="12" fill="url(#maleGradHanging)"/>

  <!-- Vertical Torso hanging from shoulders -->
  <path d="M 135 74 L 135 125" stroke="url(#maleGradHanging)" stroke-width="13" stroke-linecap="round"/>

  <!-- Both Legs Raised Horizontally at 90 degrees to Torso -->
  <path d="M 135 125 L 195 122" stroke="url(#maleGradHanging)" stroke-width="11" stroke-linecap="round"/>
  <!-- Feet pointed -->
  <path d="M 195 122 L 208 124" stroke="url(#maleGradHanging)" stroke-width="8" stroke-linecap="round"/>

  <!-- Abdominal / Core Contraction Highlight -->
  <circle cx="138" cy="112" r="5" fill="#e65100"/>
  <!-- Curved motion arrow from bottom up to 90 deg -->
  <path d="M 152 165 C 175 160, 185 142, 185 132" fill="none" stroke="#e65100" stroke-width="2.2" stroke-linecap="round"/>
  <polygon points="185,126 180,135 190,135" fill="#e65100"/>
</svg>"""

# 10. Standing Dumbbell Lateral Raise
svg_lateral_raise = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgLatRaise" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fafaf9"/>
      <stop offset="100%" stop-color="#f5f5f4"/>
    </linearGradient>
    <linearGradient id="maleGradLatRaise" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#292524"/>
      <stop offset="100%" stop-color="#44403c"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgLatRaise)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#d6d3d1" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="158" height="22" rx="6" fill="#f5f5f4" stroke="#a8a29e" stroke-width="1.2"/>
  <text x="97" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#292524" text-anchor="middle">STANDING DUMBBELL LATERAL RAISE</text>

  <!-- Male Athletic Figure Front View Raising Dumbbells to Sides -->
  <!-- Head -->
  <circle cx="150" cy="54" r="14" fill="url(#maleGradLatRaise)"/>
  <!-- Torso (athletic V-taper) -->
  <path d="M 150 68 L 150 120" stroke="url(#maleGradLatRaise)" stroke-width="15" stroke-linecap="round"/>
  <!-- Legs (shoulder width athletic stance) -->
  <path d="M 145 120 L 138 174" stroke="url(#maleGradLatRaise)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 155 120 L 162 174" stroke="url(#maleGradLatRaise)" stroke-width="10" stroke-linecap="round"/>

  <!-- Left Arm Extended Laterally to Shoulder Height (slight elbow bend) -->
  <path d="M 142 76 L 102 78 L 74 82" fill="none" stroke="url(#maleGradLatRaise)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Left Dumbbell -->
  <rect x="68" y="78" width="6" height="16" rx="2" fill="#0f172a"/>
  <rect x="74" y="83" width="8" height="5" rx="1" fill="#64748b"/>
  <rect x="82" y="78" width="6" height="16" rx="2" fill="#0f172a"/>

  <!-- Right Arm Extended Laterally to Shoulder Height -->
  <path d="M 158 76 L 198 78 L 226 82" fill="none" stroke="url(#maleGradLatRaise)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Right Dumbbell -->
  <rect x="212" y="78" width="6" height="16" rx="2" fill="#0f172a"/>
  <rect x="218" y="83" width="8" height="5" rx="1" fill="#64748b"/>
  <rect x="226" y="78" width="6" height="16" rx="2" fill="#0f172a"/>

  <!-- Lateral Deltoid Highlights -->
  <circle cx="138" cy="76" r="4.5" fill="#e65100"/>
  <circle cx="162" cy="76" r="4.5" fill="#e65100"/>
  <!-- Curved lift arrows -->
  <path d="M 95 120 C 85 110, 78 98, 76 88" fill="none" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="76,84 72,92 80,91" fill="#e65100"/>
  <path d="M 205 120 C 215 110, 222 98, 224 88" fill="none" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="224,84 220,91 228,92" fill="#e65100"/>
</svg>"""

# 11. Barbell Curl
svg_barbell_curl = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgBBCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff1f2"/>
      <stop offset="100%" stop-color="#ffe4e6"/>
    </linearGradient>
    <linearGradient id="maleGradCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9f1239"/>
      <stop offset="100%" stop-color="#881337"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgBBCurl)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#fda4af" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="138" height="22" rx="6" fill="#fff1f2" stroke="#fb7185" stroke-width="1.2"/>
  <text x="87" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#9f1239" text-anchor="middle">STANDING BARBELL CURL</text>

  <!-- Male Athletic Figure Standing Side Profile Curled Up -->
  <!-- Head -->
  <circle cx="140" cy="56" r="14" fill="url(#maleGradCurl)"/>
  <!-- Torso (upright posture, shoulders back) -->
  <path d="M 140 70 L 142 124" stroke="url(#maleGradCurl)" stroke-width="14" stroke-linecap="round"/>
  <!-- Legs (straight athletic stance) -->
  <path d="M 142 124 L 144 174" stroke="url(#maleGradCurl)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 136 174 L 160 174" stroke="url(#maleGradCurl)" stroke-width="7" stroke-linecap="round"/>

  <!-- Upper Arm pinned strictly to side -->
  <path d="M 142 78 L 144 108" stroke="url(#maleGradCurl)" stroke-width="8" stroke-linecap="round"/>
  <!-- Forearm curling Barbell up to upper chest -->
  <path d="M 144 108 L 168 84" stroke="url(#maleGradCurl)" stroke-width="8" stroke-linecap="round"/>

  <!-- Straight Barbell held in front of chest -->
  <line x1="120" y1="84" x2="216" y2="84" stroke="#64748b" stroke-width="4.5" stroke-linecap="round"/>
  <!-- Weight Plates -->
  <rect x="124" y="70" width="8" height="28" rx="2" fill="#0f172a"/>
  <rect x="204" y="70" width="8" height="28" rx="2" fill="#0f172a"/>

  <!-- Biceps Peak Contraction Highlight -->
  <circle cx="154" cy="94" r="5" fill="#e65100"/>
  <!-- Arc motion arrow -->
  <path d="M 172 130 C 182 120, 182 100, 175 88" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="172,84 180,88 174,94" fill="#e65100"/>
</svg>"""

# 12. Hammer Curl
svg_hammer_curl = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgHammerCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fffbeb"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
    <linearGradient id="maleGradHammer" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#92400e"/>
      <stop offset="100%" stop-color="#78350f"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgHammerCurl)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#fcd34d" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="138" height="22" rx="6" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.2"/>
  <text x="87" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#92400e" text-anchor="middle">DUMBBELL HAMMER CURL</text>

  <!-- Male Athletic Figure Side Profile (Neutral Grip Hammer) -->
  <circle cx="140" cy="56" r="14" fill="url(#maleGradHammer)"/>
  <path d="M 140 70 L 142 124" stroke="url(#maleGradHammer)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 142 124 L 144 174" stroke="url(#maleGradHammer)" stroke-width="11" stroke-linecap="round"/>
  <path d="M 136 174 L 160 174" stroke="url(#maleGradHammer)" stroke-width="7" stroke-linecap="round"/>

  <!-- Upper Arm at side -->
  <path d="M 142 78 L 144 108" stroke="url(#maleGradHammer)" stroke-width="8" stroke-linecap="round"/>
  <!-- Forearm in neutral 90 deg hammer position -->
  <path d="M 144 108 L 176 96" stroke="url(#maleGradHammer)" stroke-width="8" stroke-linecap="round"/>

  <!-- Vertical Dumbbell in Neutral Grip (thumbs up) -->
  <rect x="174" y="84" width="8" height="26" rx="2" fill="#475569"/>
  <rect x="170" y="74" width="16" height="10" rx="2" fill="#0f172a"/>
  <rect x="170" y="110" width="16" height="10" rx="2" fill="#0f172a"/>

  <!-- Brachialis & Forearm Highlight -->
  <circle cx="158" cy="100" r="4.5" fill="#e65100"/>
  <!-- Upward curl arrow -->
  <path d="M 172 135 C 185 125, 188 110, 186 98" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="186,93 181,101 190,101" fill="#e65100"/>
</svg>"""

# 13. Cable Rope Triceps Pushdown
svg_rope_pushdown = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgRopePush" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0f9ff"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="maleGradRope" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#075985"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgRopePush)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="152" height="22" rx="6" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="94" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#0369a1" text-anchor="middle">TRICEPS ROPE PUSHDOWN</text>

  <!-- High Cable Machine on Right -->
  <rect x="238" y="35" width="22" height="140" rx="3" fill="#334155"/>
  <circle cx="218" cy="46" r="8" fill="#64748b"/>
  <!-- Cable down to hands -->
  <line x1="218" y1="46" x2="174" y2="114" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="4,2"/>

  <!-- Male Athletic Figure Standing at Cable (slight forward hinge) -->
  <circle cx="132" cy="68" r="13" fill="url(#maleGradRope)"/>
  <path d="M 132 80 L 140 128" stroke="url(#maleGradRope)" stroke-width="13" stroke-linecap="round"/>
  <!-- Athletic staggered stance -->
  <path d="M 140 128 L 132 174" stroke="url(#maleGradRope)" stroke-width="10" stroke-linecap="round"/>
  <path d="M 140 128 L 158 174" stroke="url(#maleGradRope)" stroke-width="10" stroke-linecap="round"/>

  <!-- Upper Arm pinned at ribs -->
  <path d="M 138 88 L 144 116" stroke="url(#maleGradRope)" stroke-width="8" stroke-linecap="round"/>
  <!-- Forearms extending rope down & outward -->
  <path d="M 144 116 L 174 136" stroke="url(#maleGradRope)" stroke-width="8" stroke-linecap="round"/>

  <!-- Flared Rope Attachment with Knobs -->
  <path d="M 174 114 L 174 136 L 180 144" fill="none" stroke="#d97706" stroke-width="3" stroke-linecap="round"/>
  <circle cx="180" cy="144" r="3.5" fill="#b45309"/>

  <!-- Triceps Horseshoe Activation Highlight -->
  <path d="M 138 94 L 146 112" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <!-- Downward push arrow -->
  <path d="M 166 110 L 174 132" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="176,137 169,130 179,127" fill="#e65100"/>
</svg>"""

# 14. Skull Crushers (Lying EZ-Bar Triceps Extension)
svg_skull_crushers = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgSkullCrush" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#faf5ff"/>
      <stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>
    <linearGradient id="maleGradSkull" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6b21a8"/>
      <stop offset="100%" stop-color="#4c1d95"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgSkullCrush)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#d8b4fe" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="158" height="22" rx="6" fill="#faf5ff" stroke="#c084fc" stroke-width="1.2"/>
  <text x="97" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#6b21a8" text-anchor="middle">EZ-BAR SKULL CRUSHERS</text>

  <!-- Flat Bench -->
  <line x1="75" y1="174" x2="75" y2="132" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="195" y1="174" x2="195" y2="132" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="60" y1="128" x2="205" y2="128" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>

  <!-- Male Lifter Flat on Bench -->
  <circle cx="80" cy="116" r="13" fill="url(#maleGradSkull)"/>
  <path d="M 94 120 L 165 120" stroke="url(#maleGradSkull)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 165 120 L 195 128 L 202 174" fill="none" stroke="url(#maleGradSkull)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Upper Arms Vertical pointing at ceiling (fixed elbow position) -->
  <line x1="118" y1="116" x2="118" y2="76" stroke="url(#maleGradSkull)" stroke-width="8" stroke-linecap="round"/>
  <!-- Forearms hinged back toward forehead with EZ-bar -->
  <line x1="118" y1="76" x2="88" y2="84" stroke="url(#maleGradSkull)" stroke-width="7" stroke-linecap="round"/>

  <!-- EZ-Curl Bar above Forehead -->
  <path d="M 82 76 L 86 86 L 90 82" fill="none" stroke="#64748b" stroke-width="4.5" stroke-linecap="round"/>
  <rect x="74" y="70" width="6" height="24" rx="2" fill="#0f172a"/>

  <!-- Triceps Extension Highlight -->
  <circle cx="118" cy="88" r="4.5" fill="#e65100"/>
  <!-- Extension upward arc arrow -->
  <path d="M 90 74 C 95 62, 108 58, 118 60" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="122,62 114,57 116,66" fill="#e65100"/>
</svg>"""

# 15. Dumbbell Chest Flyes
svg_db_flyes = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgDBFlyes" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff7ed"/>
      <stop offset="100%" stop-color="#fed7aa"/>
    </linearGradient>
    <linearGradient id="maleGradFlyes" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c2410c"/>
      <stop offset="100%" stop-color="#9a3412"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgDBFlyes)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#fdba74" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="138" height="22" rx="6" fill="#fff7ed" stroke="#f97316" stroke-width="1.2"/>
  <text x="87" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#c2410c" text-anchor="middle">DUMBBELL CHEST FLYES</text>

  <!-- Flat Bench -->
  <line x1="75" y1="174" x2="75" y2="132" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="195" y1="174" x2="195" y2="132" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
  <line x1="60" y1="128" x2="205" y2="128" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>

  <!-- Male Lifter Flat on Bench -->
  <circle cx="80" cy="116" r="13" fill="url(#maleGradFlyes)"/>
  <path d="M 94 120 L 165 120" stroke="url(#maleGradFlyes)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 165 120 L 195 128 L 202 174" fill="none" stroke="url(#maleGradFlyes)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Wide Arc Arms Opening (Flye movement) -->
  <path d="M 124 116 C 118 86, 108 72, 92 64" fill="none" stroke="url(#maleGradFlyes)" stroke-width="7" stroke-linecap="round"/>
  <path d="M 134 116 C 140 86, 150 72, 168 64" fill="none" stroke="url(#maleGradFlyes)" stroke-width="7" stroke-linecap="round"/>

  <!-- Dumbbells in Palms-Facing Arc -->
  <rect x="84" y="60" width="14" height="6" rx="2" fill="#475569" transform="rotate(-25 91 63)"/>
  <rect x="162" y="60" width="14" height="6" rx="2" fill="#475569" transform="rotate(25 169 63)"/>

  <!-- Chest Stretch & Squeeze Highlight -->
  <circle cx="129" cy="114" r="5" fill="#e65100"/>
  <!-- Inward hug motion arrows -->
  <path d="M 90 54 C 104 46, 120 46, 128 50" fill="none" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="132,52 125,46 123,55" fill="#e65100"/>
</svg>"""

# 16. Lying Leg Curl Machine
svg_lying_leg_curl = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgLyingCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf4ff"/>
      <stop offset="100%" stop-color="#f5d0fe"/>
    </linearGradient>
    <linearGradient id="maleGradLying" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#701a75"/>
      <stop offset="100%" stop-color="#4a044e"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgLyingCurl)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#e879f9" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="148" height="22" rx="6" fill="#fdf4ff" stroke="#d946ef" stroke-width="1.2"/>
  <text x="92" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#701a75" text-anchor="middle">LYING LEG CURL MACHINE</text>

  <!-- Angled Prone Bench Frame -->
  <line x1="70" y1="174" x2="70" y2="132" stroke="#475569" stroke-width="5"/>
  <line x1="175" y1="174" x2="175" y2="132" stroke="#475569" stroke-width="5"/>
  <!-- Angled Pad (V-shaped hip relief pad) -->
  <line x1="60" y1="126" x2="120" y2="122" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>
  <line x1="120" y1="122" x2="180" y2="132" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>

  <!-- Male Lifter Prone (Face Down) -->
  <circle cx="68" cy="114" r="12" fill="url(#maleGradLying)"/>
  <!-- Torso & Hips lying prone -->
  <path d="M 78 118 L 128 120" stroke="url(#maleGradLying)" stroke-width="13" stroke-linecap="round"/>
  <path d="M 76 126 L 62 136" stroke="url(#maleGradLying)" stroke-width="6" stroke-linecap="round"/> <!-- hand holding handle -->

  <!-- Thighs on pad -->
  <path d="M 128 120 L 175 130" stroke="url(#maleGradLying)" stroke-width="11" stroke-linecap="round"/>
  <!-- Lower Legs curled up to 90 degrees against roller pad -->
  <path d="M 175 130 L 165 82" stroke="url(#maleGradLying)" stroke-width="9" stroke-linecap="round"/>

  <!-- Machine Lever Arm & Roller Pad behind Achilles/Ankles -->
  <circle cx="178" cy="132" r="5" fill="#64748b"/>
  <line x1="178" y1="132" x2="168" y2="82" stroke="#94a3b8" stroke-width="3"/>
  <circle cx="168" cy="82" r="7" fill="#0f172a"/>

  <!-- Hamstrings Contraction Highlight -->
  <path d="M 140 118 L 168 124" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <!-- Curled motion arrow -->
  <path d="M 215 135 C 215 105, 195 85, 180 82" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="175,82 184,86 182,78" fill="#e65100"/>
</svg>"""

# 17. Seated Leg Curl Machine
svg_seated_leg_curl = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgSeatedCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf4ff"/>
      <stop offset="100%" stop-color="#fae8ff"/>
    </linearGradient>
    <linearGradient id="maleGradSeatedCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#86198f"/>
      <stop offset="100%" stop-color="#701a75"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgSeatedCurl)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#f0abfc" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="154" height="22" rx="6" fill="#fdf4ff" stroke="#e879f9" stroke-width="1.2"/>
  <text x="95" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="#86198f" text-anchor="middle">SEATED LEG CURL MACHINE</text>

  <!-- Seated Machine Chair & Frame -->
  <line x1="110" y1="80" x2="110" y2="140" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>
  <line x1="110" y1="140" x2="162" y2="140" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>
  <line x1="105" y1="174" x2="105" y2="120" stroke="#475569" stroke-width="4"/>
  <line x1="150" y1="174" x2="150" y2="140" stroke="#475569" stroke-width="4"/>

  <!-- Male Lifter Seated in Machine -->
  <circle cx="124" cy="74" r="13" fill="url(#maleGradSeatedCurl)"/>
  <path d="M 124 86 L 126 138" stroke="url(#maleGradSeatedCurl)" stroke-width="13" stroke-linecap="round"/>
  <!-- Thighs pinned under thigh pad -->
  <path d="M 126 138 L 175 138" stroke="url(#maleGradSeatedCurl)" stroke-width="11" stroke-linecap="round"/>
  <!-- Thigh Hold-Down Pad -->
  <rect x="145" y="126" width="28" height="7" rx="3" fill="#0f172a"/>

  <!-- Lower Legs curled downward under seat -->
  <path d="M 175 138 L 165 174" stroke="url(#maleGradSeatedCurl)" stroke-width="9" stroke-linecap="round"/>

  <!-- Machine Pivot Axis & Lower Roller Pad behind ankles -->
  <circle cx="178" cy="140" r="5" fill="#64748b"/>
  <line x1="178" y1="140" x2="168" y2="174" stroke="#94a3b8" stroke-width="3"/>
  <circle cx="168" cy="174" r="6.5" fill="#0f172a"/>

  <!-- Hamstrings Contraction Highlight -->
  <path d="M 136 142 L 165 142" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <!-- Downward sweep motion arrow -->
  <path d="M 205 144 C 205 160, 190 172, 178 174" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="173,174 182,171 180,179" fill="#e65100"/>
</svg>"""

# 18. Standing Calf Raise Machine
svg_calf_raise = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgCalfRaise" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <linearGradient id="maleGradCalf" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#166534"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgCalfRaise)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#86efac" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="162" height="22" rx="6" fill="#f0fdf4" stroke="#4ade80" stroke-width="1.2"/>
  <text x="99" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#166534" text-anchor="middle">STANDING CALF RAISE MACHINE</text>

  <!-- Machine Tower on Left & Elevated Calf Block on Floor -->
  <rect x="55" y="45" width="20" height="130" rx="2" fill="#334155"/>
  <!-- Elevated Toe Block -->
  <rect x="140" y="166" width="30" height="9" rx="2" fill="#0f172a"/>

  <!-- Machine Shoulder Pads resting on lifter -->
  <line x1="65" y1="62" x2="148" y2="62" stroke="#64748b" stroke-width="4"/>
  <rect x="135" y="58" width="25" height="10" rx="4" fill="#1e293b"/>

  <!-- Male Athletic Figure Standing Erect under Shoulder Pads -->
  <!-- Head -->
  <circle cx="150" cy="50" r="13" fill="url(#maleGradCalf)"/>
  <!-- Torso & Hips straight -->
  <path d="M 148 64 L 148 118" stroke="url(#maleGradCalf)" stroke-width="14" stroke-linecap="round"/>
  <!-- Legs straight -->
  <path d="M 148 118 L 148 160" stroke="url(#maleGradCalf)" stroke-width="11" stroke-linecap="round"/>

  <!-- Feet on block: Balls of feet on block, Heels elevated high (peak contraction) -->
  <path d="M 148 160 L 155 166" stroke="url(#maleGradCalf)" stroke-width="7" stroke-linecap="round"/>

  <!-- Calf Muscles (Gastrocnemius / Soleus) Peak Flex Highlight -->
  <path d="M 144 135 L 144 150" stroke="#e65100" stroke-width="4" stroke-linecap="round"/>
  <circle cx="144" cy="142" r="4.5" fill="#e65100"/>

  <!-- Motion arrow upward from heels -->
  <path d="M 166 172 L 166 150" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
  <polygon points="166,145 162,153 170,153" fill="#e65100"/>
</svg>"""

# 19. Seated Palms-Up Wrist Curl
svg_wrist_curl = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgWristCurl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="maleGradWrist" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="300" height="200" rx="14" fill="url(#bgWristCurl)"/>
  
  <!-- Floor line -->
  <line x1="25" y1="175" x2="275" y2="175" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Badge -->
  <rect x="18" y="14" width="168" height="22" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="102" y="29" font-family="'IBM Plex Mono', system-ui, sans-serif" font-size="8" font-weight="bold" fill="#334155" text-anchor="middle">SEATED PALMS-UP WRIST CURL</text>

  <!-- Bench / Seat -->
  <line x1="80" y1="174" x2="80" y2="135" stroke="#475569" stroke-width="5"/>
  <line x1="140" y1="174" x2="140" y2="135" stroke="#475569" stroke-width="5"/>
  <line x1="70" y1="130" x2="150" y2="130" stroke="#1e293b" stroke-width="9" stroke-linecap="round"/>

  <!-- Male Athletic Figure Seated, Forearms Resting on Thighs -->
  <!-- Head & Forward leaning torso -->
  <circle cx="118" cy="74" r="13" fill="url(#maleGradWrist)"/>
  <path d="M 118 86 L 105 132" stroke="url(#maleGradWrist)" stroke-width="13" stroke-linecap="round"/>
  <!-- Thighs horizontal over knees -->
  <path d="M 105 132 L 175 134 L 180 174" fill="none" stroke="url(#maleGradWrist)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 172 174 L 194 174" stroke="url(#maleGradWrist)" stroke-width="7" stroke-linecap="round"/>

  <!-- Forearms resting flat on thighs, wrists hanging past knees -->
  <path d="M 116 94 L 140 125 L 182 125" fill="none" stroke="url(#maleGradWrist)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Hands Curling Barbell Upwards (Palms Facing Up) -->
  <path d="M 182 125 L 190 114" stroke="url(#maleGradWrist)" stroke-width="7" stroke-linecap="round"/>
  
  <!-- Barbell in fingers/palms -->
  <line x1="170" y1="112" x2="225" y2="112" stroke="#64748b" stroke-width="4.5" stroke-linecap="round"/>
  <rect x="172" y="102" width="6" height="20" rx="2" fill="#0f172a"/>
  <rect x="218" y="102" width="6" height="20" rx="2" fill="#0f172a"/>

  <!-- Forearm Flexors Highlight -->
  <path d="M 148 128 L 178 128" stroke="#e65100" stroke-width="3" stroke-linecap="round"/>
  <circle cx="188" cy="116" r="4" fill="#e65100"/>
  <!-- Wrist curl upward arrow -->
  <path d="M 194 130 C 198 126, 198 118, 195 110" fill="none" stroke="#e65100" stroke-width="1.8" stroke-linecap="round"/>
  <polygon points="194,106 191,114 199,112" fill="#e65100"/>
</svg>"""

FILES = {
    'ex-barbell-back-squat.svg': svg_back_squat,
    'ex-conventional-deadlift.svg': svg_deadlift,
    'ex-incline-barbell-bench-press.svg': svg_incline_barbell,
    'ex-incline-dumbbell-press.svg': svg_incline_dumbbell,
    'ex-dumbbell-bench-press.svg': svg_dumbbell_bench,
    'ex-seated-cable-row.svg': svg_cable_row,
    'ex-leg-press.svg': svg_leg_press,
    'ex-seated-dumbbell-shoulder-press.svg': svg_seated_db_press,
    'ex-hanging-leg-raise.svg': svg_hanging_leg_raise,
    'ex-standing-dumbbell-lateral-raise.svg': svg_lateral_raise,
    'ex-barbell-curl.svg': svg_barbell_curl,
    'ex-hammer-curl.svg': svg_hammer_curl,
    'ex-triceps-rope-pushdown.svg': svg_rope_pushdown,
    'ex-skull-crushers.svg': svg_skull_crushers,
    'ex-dumbbell-chest-flyes.svg': svg_db_flyes,
    'ex-lying-leg-curl-machine.svg': svg_lying_leg_curl,
    'ex-seated-leg-curl-machine.svg': svg_seated_leg_curl,
    'ex-standing-calf-raise-machine.svg': svg_calf_raise,
    'ex-seated-palms-up-wrist-curl.svg': svg_wrist_curl,
}

for fname, content in FILES.items():
    filepath = os.path.join(SVG_DIR, fname)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    size = os.path.getsize(filepath)
    print(f"Created: {fname:40} | {size} bytes")

print(f"\nSuccessfully generated all {len(FILES)} SVGs in {SVG_DIR}!")
