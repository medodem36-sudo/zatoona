import sys
sys.stdout.reconfigure(encoding="utf-8")

# Let's test the routine-to-drills selection logic

WARMUP_DRILLS_DB = {
    'cardio': {
        'id': 'gen-cardio',
        'nameAr': 'إحماء عام (كارديو خفيف)',
        'name': 'General Light Cardio',
        'type': 'إحماء عام',
        'typeKey': 'cardio',
        'target': 'الجسم كامل، تنشيط الدورة الدموية',
        'duration': '3-5 دقائق',
        'image': './assets/images/warmup/warmup-01-cardio.svg',
        'steps': [
            'ابدأ بمشي سريع أو هرولة خفيفة على السير أو دراجة ثابتة أو نط حبل خفيف.',
            'حافظ على وتيرة معتدلة تسمح لك بالتنفس المنتظم دون إجهاد شديد.',
            'الهدف هو رفع حرارة العضلات تدريجيًا وبدء التعرق الخفيف وتهيئة المفاصل.'
        ]
    }
}

# Routine test cases
test_routines = [
    ('A', 'تمرينة A (سكوات وبنش وسحب)'),
    ('B', 'تمرينة B (ديدليفت ورو وضغط)'),
    ('fb_a', 'فول بودي A'),
    ('fb_b', 'فول بودي B'),
    ('ppl_push', 'بوش (Push)'),
    ('ppl_pull', 'بول (Pull)'),
    ('ppl_legs', 'ليجز (Legs)'),
    ('ul_upper', 'أبر (Upper)'),
    ('ul_lower', 'لور (Lower)'),
    ('bro_chest', 'يوم الصدر'),
    ('bro_legs', 'يوم الأرجل'),
    ('unknown_custom', 'روتين مخصص غير معروف')
]

print("Warmup Generator Logic verification ready.")
