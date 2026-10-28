"""
Automated Acceptance Test Suite: Prayer Qibla Compass (Proposal #10)
Phase 13.8B: Spherical Trigonometry Qibla Bearing, Distance, Offline Cities, SVG Compass Dial, and Device Heading Alignment
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def test(name, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {name}")
        passed_count += 1
    else:
        print(f"  [FAIL] {name} - {details}")
        failed_count += 1

def run_tests():
    global passed_count, failed_count
    print("=" * 80)
    print("PHASE 13.8B ACCEPTANCE TEST SUITE: PRAYER QIBLA COMPASS (PROPOSAL #10)")
    print("=" * 80)

    html_path = os.path.abspath('index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=375,812')

    driver = webdriver.Chrome(options=opts)
    driver.get(file_url)
    time.sleep(1.0)

    def js(script):
        return driver.execute_script(script)

    try:
        # Group 1: DOM Elements & Functions Presence
        print("\n--- Group 1: DOM Elements & Functions Presence ---")
        dom_check = js("""
            return {
                hasCard: !!document.getElementById('qiblaCard'),
                hasCalc: typeof window.calculateQibla === 'function',
                hasCityQibla: typeof window.getCityQibla === 'function',
                hasCurrentData: typeof window.getCurrentQiblaData === 'function',
                hasRender: typeof window.renderQiblaCard === 'function',
                hasStart: typeof window.startLiveCompass === 'function',
                hasStop: typeof window.stopLiveCompass === 'function'
            };
        """)

        test("#qiblaCard container exists in DOM", dom_check.get('hasCard'))
        test("window.calculateQibla is a function", dom_check.get('hasCalc'))
        test("window.getCityQibla is a function", dom_check.get('hasCityQibla'))
        test("window.getCurrentQiblaData is a function", dom_check.get('hasCurrentData'))
        test("window.renderQiblaCard is a function", dom_check.get('hasRender'))
        test("window.startLiveCompass is a function", dom_check.get('hasStart'))
        test("window.stopLiveCompass is a function", dom_check.get('hasStop'))

        # Group 2: Spherical Trigonometry Mathematical Accuracy
        print("\n--- Group 2: Spherical Trigonometry Mathematical Accuracy ---")
        math_check = js("""
            const cairo = window.calculateQibla(30.0444, 31.2357);
            const alex = window.calculateQibla(31.2001, 29.9187);
            const minya = window.calculateQibla(28.1099, 30.7503);

            return {
                cairoBearing: cairo.bearing,
                cairoDist: cairo.distanceKm,
                cairoDir: cairo.compassDirection,
                alexBearing: alex.bearing,
                alexDist: alex.distanceKm,
                minyaBearing: minya.bearing,
                minyaDist: minya.distanceKm
            };
        """)

        test("Cairo Qibla bearing is ~136.1° (within 0.5°)", abs(math_check.get('cairoBearing') - 136.1) < 0.5)
        test("Cairo distance to Kaaba is ~1287 km (within 10 km)", abs(math_check.get('cairoDist') - 1287) < 10)
        test("Cairo compass direction is جنوب شرق", math_check.get('cairoDir') == 'جنوب شرق')
        test("Alexandria Qibla bearing is ~135.4° (within 0.5°)", abs(math_check.get('alexBearing') - 135.4) < 0.5)
        test("Minya Qibla bearing is ~127.1° (within 0.5°)", abs(math_check.get('minyaBearing') - 127.1) < 0.5)

        # Group 3: Predefined Offline Cities Integration
        print("\n--- Group 3: Predefined Offline Cities Integration ---")
        cities_check = js("""
            const cairoCity = window.getCityQibla('Cairo');
            const minyaCity = window.getCityQibla('Minya');
            const alexCity = window.getCityQibla('Alexandria');

            return {
                cairoName: cairoCity.cityName,
                minyaName: minyaCity.cityName,
                alexName: alexCity.cityName
            };
        """)

        test("City Qibla for Cairo returns 'القاهرة'", cities_check.get('cairoName') == 'القاهرة')
        test("City Qibla for Minya returns 'المنيا'", cities_check.get('minyaName') == 'المنيا')
        test("City Qibla for Alexandria returns 'الإسكندرية'", cities_check.get('alexName') == 'الإسكندرية')

        # Group 4: Interactive Compass UI & SVG Dial Rendering
        print("\n--- Group 4: Interactive Compass UI & SVG Dial Rendering ---")
        ui_check = js("""
            window.routeNotificationClick({ mode: 'prayer' });
            window.renderQiblaCard();

            const card = document.getElementById('qiblaCard');
            const dial = document.getElementById('qiblaSvgDial');
            const btnCompass = document.getElementById('btnToggleCompass');
            const btnGps = document.getElementById('btnGpsQibla');

            return {
                cardHasContent: !!card && card.innerHTML.length > 50,
                hasDial: !!dial,
                hasCompassBtn: !!btnCompass,
                hasGpsBtn: !!btnGps,
                hasKaabaEmblem: card ? card.innerHTML.includes('🕋') : false
            };
        """)

        test("Qibla card renders rich visual content", ui_check.get('cardHasContent'))
        test("SVG compass dial is rendered in the DOM", ui_check.get('hasDial'))
        test("#btnToggleCompass button exists", ui_check.get('hasCompassBtn'))
        test("#btnGpsQibla button exists", ui_check.get('hasGpsBtn'))
        test("Kaaba emblem (🕋) is displayed on the needle tip", ui_check.get('hasKaabaEmblem'))

        # Group 5: Compass Orientation State & Heading Alignment Simulation
        print("\n--- Group 5: Compass Orientation State & Heading Alignment Simulation ---")
        sim_check = js("""
            return (async () => {
                await window.startLiveCompass();
                const btnAfterStart = document.getElementById('btnToggleCompass').textContent;
                const isLiveAfterStart = btnAfterStart.includes('إيقاف');

                // Simulate device heading aligned with current city Qibla
                const data = window.getCurrentQiblaData();
                const bearing = data.bearing;

                let ev = new Event('deviceorientation');
                Object.defineProperty(ev, 'webkitCompassHeading', { value: bearing });
                Object.defineProperty(ev, 'alpha', { value: (360 - bearing) % 360 });
                window.dispatchEvent(ev);

                const statusText = document.getElementById('qiblaStatusMsg').textContent;
                const isAligned = statusText.includes('اتجاه القبلة تمامًا');

                window.stopLiveCompass();
                const btnAfterStop = document.getElementById('btnToggleCompass').textContent;
                const isStopped = btnAfterStop.includes('بوصلة حية');

                return {
                    isLiveAfterStart,
                    isAligned,
                    isStopped
                };
            })();
        """)

        test("startLiveCompass activates live compass mode", sim_check.get('isLiveAfterStart'))
        test("Heading within tolerance triggers 'أنت في اتجاه القبلة تمامًا' alignment", sim_check.get('isAligned'))
        test("stopLiveCompass deactivates live compass correctly", sim_check.get('isStopped'))

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)

    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
