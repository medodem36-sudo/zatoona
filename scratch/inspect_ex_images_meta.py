# -*- coding: utf-8 -*-
import urllib.request, os, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

files = [
    'Kettle_bell_squats.jpg',
    'Bench_press_dumbbell_1.svg',
    'Girl_doing_lat_pulldown_exercise.jpg',
    'Girl_doing_dumbbell_shoulder_press_02.jpg',
    'Girl_exercising_doing_a_plank.jpg',
    'Rear_deltoid_row_barbell_1.svg',
    'Barbell_dead_lifts_1.svg',
    'Reverse_grips_bent_over_barbell_rows_1.svg',
    'Exercise_Press_Up.png',
    'U.S._Air_Force_Senior_Airman_Brandon_Stout_performs_pull-ups.jpg',
    'Abdominal_curl-CDC_strength_training_for_older_adults.gif',
    'Lunge-CDC_strength_training_for_older_adults.gif',
]

headers = {'User-Agent': 'Mozilla/5.0'}
for f in files:
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{f}&prop=imageinfo&iiprop=extmetadata|url&format=json'
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            d = json.loads(r.read().decode('utf-8'))
            pages = d.get('query', {}).get('pages', {})
            for k, v in pages.items():
                meta = v.get('imageinfo', [{}])[0].get('extmetadata', {})
                cats = meta.get('Categories', {}).get('value', 'N/A')
                desc = meta.get('ImageDescription', {}).get('value', 'N/A')
                lic = meta.get('LicenseShortName', {}).get('value', 'N/A')
                print(f"File: {f}")
                print(f"  License: {lic}")
                print(f"  Categories: {cats[:100]}")
                print(f"  Desc: {desc[:100]}")
    except Exception as e:
        print(f"File {f} error: {e}")
