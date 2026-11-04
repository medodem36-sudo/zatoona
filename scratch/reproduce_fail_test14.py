import sys, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=opts)

INDEX_PATH = os.path.abspath('index.html')
driver.get(f"file:///{INDEX_PATH}")
time.sleep(1)

# Run test 10 through 14 in the exact sequence as test_phase3_gym_engine.py
print("Running test 10...")
driver.execute_script("""
    openGymBigNumbersOverlay('squat');
    document.getElementById('gbnPlusWeight').click();
    document.getElementById('gbnDoneSetBtn').click();
    document.getElementById('gbnSkipRest').click();
    document.getElementById('gbnCloseBtn').click();
""")

print("Running test 11...")
driver.execute_script("""
    openGymTempoModal();
    const sel = document.getElementById('tempoPresetSelect');
    sel.value = '3-0-1-0';
    sel.dispatchEvent(new Event('change'));
    document.getElementById('btnToggleTempoPlay').click();
    document.getElementById('btnToggleTempoPlay').click();
    document.getElementById('btnCloseTempoModal').click();
""")

print("Running test 12...")
driver.execute_script("""
    navigateTo('gym');
    for(let i=0; i<weekDates.length; i++){
        const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
        if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
            selectedIdx = i;
            break;
        }
    }
    renderExercises();
    openGymPainTrackerModal('squat');
    const exSel = document.getElementById('painExerciseSelect');
    if(exSel.options.length > 0){
        exSel.selectedIndex = 0;
    }
    const chosenKey = exSel.value;
    const jSel = document.getElementById('painJointSelect');
    jSel.value = 'الركبة';
    const iSel = document.getElementById('painIntensitySelect');
    iSel.value = '6';
    document.getElementById('painNotesInput').value = 'ألم خفيف أثناء أقصى النزول';
    document.getElementById('btnSavePainFlag').click();
    renderExercises();
    const clearBtn = document.querySelector('[data-clear-pain-key=\"' + chosenKey + '\"]');
    if(clearBtn) clearBtn.click();
    document.getElementById('btnClosePainModal').click();
""")

print("Running test 13...")
driver.execute_script("""
    navigateTo('gym');
    for(let i=0; i<weekDates.length; i++){
        const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
        if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
            selectedIdx = i;
            break;
        }
    }
    renderExercises();
""")

print("Running test 14...")
res14 = driver.execute_script("""
    navigateTo('gym');
    for(let i=0; i<weekDates.length; i++){
        const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
        if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
            selectedIdx = i;
            break;
        }
    }
    renderExercises();

    const hud = document.getElementById('gymActiveWorkoutHud');
    const exists = (hud !== null);

    const firstChip = document.querySelector('#exercises .set-chip');
    const chipFound = !!firstChip;
    const chipClassBefore = firstChip ? firstChip.className : null;

    if(firstChip) firstChip.click();

    const chipClassAfter = firstChip ? firstChip.className : null;
    const isVisible = hud ? !hud.classList.contains('hidden') : false;
    const hudClass = hud ? hud.className : null;
    const title = document.getElementById('hudExTitle') ? document.getElementById('hudExTitle').textContent : null;

    // Check exState
    const iso = toISO(weekDates[selectedIdx]);
    const exSt = window.exState;

    return { exists, isVisible, chipFound, chipClassBefore, chipClassAfter, hudClass, title, iso, exSt };
""")

print("Test 14 output:")
for k, v in res14.items():
    print(f"  {k}: {v}")

driver.quit()
