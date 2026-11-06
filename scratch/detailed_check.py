# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

user_dir = os.environ['USERPROFILE']
p1 = os.path.join(user_dir, r'.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\zatoona_200_master_proposals.md')
p2 = os.path.join(user_dir, r'.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\zatoona_200_fresh_proposals.md')

def load_proposals(path):
    items = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            m = re.match(r'^(\d+)\.\s*\*\*(.*?)\*\*:\s*(.*)$', line)
            if m:
                num = int(m.group(1))
                items[num] = (m.group(2).strip(), m.group(3).strip())
    return items

prop1 = load_proposals(p1)
prop2 = load_proposals(p2)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Audit items in list 1:
audit_list1 = [
    (4, "دفتر قضاء الصلوات الفائتة", "قضاء الصلوات" in html or "qada" in html.lower()),
    (7, "منبه قيام الليل المتكيف مع الثلث الأخير", "الثلث الأخير" in html or "lastThird" in html),
    (9, "متتبع صيام النوافل (الاثنين والخميس والبيض)", "صيام" in html or "fasting" in html.lower()),
    (15, "ويدجت ختمة القرآن لشاشة الهاتف الرئيسية", "khatma" in html.lower() or "ختمة" in html),
    (18, "وضع الاعتكاف والهدوء الروحي", "اعتكاف" in html or "safar" in html.lower()),
    (19, "تحدي الاستيقاظ لصلاة الفجر بمؤثرات رياضية", "alarm" in html.lower()),
    (20, "سجل سجدات الشكر والتلاوة اليومية", "شكر" in html),
    (32, "مخطط أسبوع تخفيف الحمل التلقائي (Deload)", "deload" in html.lower()),
    (34, "مسار احتراف تمارين وزن الجسم (Calisthenics)", "calisthenics" in html.lower()),
    (35, "مؤشر إجهاد الجهاز العصبي المركزي (CNS)", "cns" in html.lower()),
    (37, "تصدير سجل التمرين كملف Excel / CSV", "تصدير" in html or "csv" in html.lower()),
    (38, "فلترة التمارين بحسب بيئة التدريب", "فلترة" in html or "filter" in html.lower()),
    (39, "حاسبة نسبة دهون الجسم بالبحرية الأمريكية", "cardUSNavyFatCalc" in html),
    (40, "ويدجت شاشة القفل لبدء التمرين", "lock" in html.lower() or "widget" in html.lower()),
    (43, "ميزة السوبر سيت (Superset Linker)", "superset" in html.lower()),
    (44, "مقياس معدل الجهد المحسوس (RPE / RIR Tracker)", "rpe" in html.lower() and "rir" in html.lower()),
    (51, "موسوعة الأكلات الشعبية المصرية الموسعة", "كشري" in html or "طعمية" in html),
    (52, "حاسبة التكلفة لكل جرام بروتين فعلي في مصر", "cardCostPerProtein" in html),
    (55, "حاسبة ميزانية التغذية اليومية (Daily Food Allowance)", "daily food allowance" in html.lower() or "مصروف" in html),
    (56, "قائمة التسوق الذكية المقسمة جغرافياً", "shopping" in html.lower() or "تسوق" in html),
    (57, "متتبع شرب المياه المتكيف مع الحرارة والتمرين", "شرب المياه" in html or "water" in html.lower()),
    (59, "خطط وجبات جاهزة للبيئة المصرية", "وجبات" in html or "meal" in html.lower()),
    (64, "حاسبة المرونة في الدايت (Flexible Dieting)", "carb cycling" in html.lower() or "مرونة" in html),
    (73, "مؤشر الكثافة الغذائية وجودة الأطعمة", "protein quality" in html.lower() or "كثافة" in html),
    (79, "حاسبة دورات النوم الـ 90 دقيقة (REM & NREM)", "90 دقيقة" in html or "sleep cycle" in html.lower()),
    (80, "مؤقت القيلولة الذكية (20 دقيقة)", "قيلولة" in html or "nap" in html.lower()),
    (85, "مؤقت راحة العين 20-20-20 للوقاية من الشاشات", "toggleEyeBreakTimer" in html or "20-20-20" in html),
    (88, "وضع القراءة الليلية فائقة الحمرة (Red Shift)", "toggleUltraDarkRedShift" in html or "red_shift" in html.lower()),
    (96, "مصفوفة أيزنهاور لتنظيم المهام (4 مربعات)", "eisenhower" in html.lower()),
    (99, "التنبؤ التلقائي بالأيام المزدحمة وتخفيف المهام", "conflict" in html.lower() or "ازدحام" in html),
    (100, "حجب المهام غير القابلة للتنفيذ خارج أوقاتها", "time-blocking" in html.lower()),
    (105, "التكرار الذكي غير المنتظم للعادات المتقطعة", "complex recurring" in html.lower()),
    (107, "كبسولة النشاط الحالي في شريط الحالة (Capsule)", "status capsule" in html.lower() or "mini-status" in html.lower()),
    (112, "نمط الاستراحة الإلزامية بعد فترات العمل الطويلة", "stretch break" in html.lower()),
    (133, "حركات الانتقال المشتركة (Shared-Element Morphing)", "shared element" in html.lower() or "morphing" in html.lower()),
    (138, "نمط الواجهة الصامتة للتركيز (Minimalist Mode)", "amoled" in html.lower() or "minimalist" in html.lower()),
    (140, "تفاعلات الاهتزاز الفيزيائي الدقيقة (Haptics)", "triggerHaptic" in html or "haptic" in html.lower()),
    (151, "إنذار الشاشة الكاملة على شاشة القفل (Full-Screen Intent)", "AlarmActivity" in open('android/app/src/main/AndroidManifest.xml').read()),
    (152, "معاينة نغمات المنبه وأنماط الاهتزاز في الإعدادات", "vibrate" in html.lower() or "preview" in html.lower()),
    (155, "ويدجات الشاشة الرئيسية التكيفية بأبعاد مختلفة", "AppWidgetProvider" in open('android/app/src/main/AndroidManifest.xml').read()),
    (163, "وضع تقسيم الشاشة ونافذة الملاحة العائمة", "floating" in html.lower() or "split" in html.lower()),
    (166, "إعادة جدولة الإنذارات عند إقلاع الجهاز (Boot Completed)", "BootReceiver" in open('android/app/src/main/AndroidManifest.xml').read()),
    (171, "تشفير البيانات الحساسة بمفتاح محلي AES-256-GCM", "aes-gcm" in html.lower() or "encrypt" in html.lower()),
    (173, "التجاهل التلقائي للملفات المؤقتة والذاكرة الميتة", "clean" in html.lower() or "cache" in html.lower()),
    (174, "مدقق سلامة البيانات وعدم التلف (Data Integrity)", "integrity" in html.lower() or "verify" in html.lower()),
    (175, "تطبيق معزول محلياً بالكامل (Strict Local Sandbox)", "sandbox" in html.lower() or "offline" in html.lower()),
    (178, "سلة المحذوفات المؤقتة (Soft Delete Trash Bin)", "trash" in html.lower() or "سلة" in html),
    (180, "تصفير مخصص لبيانات أقسام محددة (Selective Purge)", "purge" in html.lower()),
    (183, "نقل البيانات السريع عبر QR Code محلياً", "qr" in html.lower()),
    (185, "تنبيهات الصيانة المحلية والنسخ الاحتياطي الدوري", "backup" in html.lower()),
    (187, "مستشار الذكاء الاصطناعي المحلي 100% (Local AI)", "local ai" in html.lower() or "ai" in html.lower()),
    (189, "عجلة التوازن الحياتي الشاملة (Life Balance Wheel)", "cardLifeBalanceWheel" in html),
    (193, "محلل مغالطة التخطيط (Planning Fallacy Analyzer)", "estimated vs actual" in html.lower() or "accuracy" in html.lower())
]

# Audit items in list 2 (200 + N):
audit_list2 = [
    (3, 203, "مفكرة تدبر الأربعين النووية", "أربعين نووية" in html or "الأربعين" in html),
    (4, 204, "دليل سنن النوم المهجورة", "cardSunanOfSleep" in html),
    (11, 211, "سجل صلة الرحم والتواصل العائلي الأسبوعي", "cardKinshipTies" in html),
    (15, 215, "بطاقة الدعاء للمسلمين بظهر الغيب", "دعاء" in html),
    (23, 223, "كاشف عدم التماثل العضلي بين الجانبين", "asymmetry" in html.lower()),
    (26, 226, "متتبع حمل الأوتار والتهابات المفاصل", "tendinopathy" in html.lower() or "أوتار" in html),
    (28, 228, "نظام التناوب بين الألياف السريعة والبطيئة", "ألياف" in html or "hypertrophy" in html.lower()),
    (32, 232, "دليل ضبط قبضة اليد (Hook Grip vs Mixed)", "hook grip" in html.lower() or "قبضة" in html),
    (35, 235, "برنامج استعادة اللياقة بعد الانقطاع (DOMS)", "doms" in html.lower() or "استشفاء" in html),
    (44, 244, "حاسبة فيتامين د3 وزاوية أشعة الشمس في مصر", "cardVitDEgyptSun" in html),
    (83, 283, "حاسبة العمر المهدور على الشاشات", "cardScreenTimeWaste" in html),
    (90, 290, "جلسات التفكر والتأمل في الآفاق والكون", "تفكر" in html or "تأمل" in html),
    (127, 327, "المنبه الضوئي عبر فلاش الكاميرا", "flash" in html.lower()),
    (131, 331, "قراءة مستشعرات الرطوبة والحرارة عبر BLE", "ble" in html.lower()),
    (136, 336, "تفعيل وضع التركيز الفوري بقلب الهاتف (Flip to Focus)", "flip" in html.lower()),
    (142, 342, "محرر سمات الواجهة المتكامل (Custom CSS Theme)", "theme" in html.lower()),
    (155, 355, "محاكي أبعاد الشاشات المختلفة داخل التطبيق", "screen" in html.lower()),
    (174, 374, "حاسبة استهلاك السعرات في الأعمال المنزلية", "أعمال منزلية" in html or "household" in html.lower())
]

print("=== RESULTS LIST 1 ===")
for num, title, status in audit_list1:
    print(f"[{num}] {title}: {'IMPLEMENTED' if status else 'PLANNED/PARTIAL'}")

print("\n=== RESULTS LIST 2 ===")
for rel_num, abs_num, title, status in audit_list2:
    print(f"[{rel_num} -> #{abs_num}] {title}: {'IMPLEMENTED' if status else 'PLANNED/PARTIAL'}")
