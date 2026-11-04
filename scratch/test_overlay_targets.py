import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

targets = [
    ("gym-modal-overlay", """.gym-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}
.gym-modal-overlay.open {
  opacity: 1;
  pointer-events: auto;
}"""),
    ("p4-modal-overlay", """.p4-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.25s ease, visibility 0.25s ease;
}
.p4-modal-overlay.open {
  opacity: 1;
  visibility: visible;
}"""),
    ("p5-modal-overlay", """.p5-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.p5-modal-overlay.active {
  opacity: 1;
  pointer-events: auto;
}"""),
    ("img-viewer-overlay", """.img-viewer-overlay{
    position:fixed; inset:0; background:rgba(0,0,0,0.8); backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px);
    z-index:1100; display:flex; align-items:center; justify-content:center; padding:12px;
    opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .img-viewer-overlay.open{ opacity:1; pointer-events:auto; }"""),
    ("backup-crypto-overlay", """.backup-crypto-overlay{
    position:fixed; inset:0; background:rgba(0,0,0,0.65); backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px);
    z-index:1050; display:flex; align-items:center; justify-content:center; padding:14px;
    opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .backup-crypto-overlay.open{ opacity:1; pointer-events:auto; }"""),
    ("battery-guide-overlay", """.battery-guide-overlay{
    position:fixed; inset:0; background:rgba(0,0,0,0.65); backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px);
    z-index:1050; display:flex; align-items:center; justify-content:center; padding:14px;
    opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .battery-guide-overlay.open{ opacity:1; pointer-events:auto; }"""),
    ("ex-img-modal-overlay", """.ex-img-modal-overlay{
    position:fixed; inset:0; background:rgba(0,0,0,0.65); backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px);
    z-index:1050; display:flex; align-items:center; justify-content:center; padding:14px;
    opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .ex-img-modal-overlay.open{ opacity:1; pointer-events:auto; }"""),
    ("str-modal-overlay", """.str-modal-overlay{
    position:fixed; top:0; left:0; width:100%; height:100%; z-index:1200;
    background:rgba(0,0,0,.55); display:flex; align-items:center; justify-content:center;
    padding:16px; opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .str-modal-overlay.open{ opacity:1; pointer-events:auto; }"""),
    ("drawer-overlay", """.drawer-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
  }
  .drawer-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }""")
]

for name, t in targets:
    found = t in c
    print(f"Target '{name}': {'FOUND ✅' if found else 'NOT FOUND ❌'}")
