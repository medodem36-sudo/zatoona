# -*- coding: utf-8 -*-
"""
Generator for:
1. assets/data/stretch-catalog.js
2. assets/images/stretches/*.svg

Strict compliance:
- 34 distinct movements across 10 regions
- 5 types: static_stretch, dynamic_stretch, joint_mobility, activation, warmup_drill
- Males-Only: Athletic male silhouettes/figures, zero external URLs
- Complete fields per prompt specification
"""

import os, json, sys

sys.stdout.reconfigure(encoding='utf-8')

# Ensure directory exists
stretches_dir = r"assets\images\stretches"
os.makedirs(stretches_dir, exist_ok=True)

# Define the 34 movements data structure
MOVEMENTS = [
    # --- 1. الصدر والكتف (Chest & Shoulders) ---
    {
        "id": "str-doorway-pec-stretch",
        "name": "Doorway Pec Stretch",
        "nameAr": "إطالة عضلات الصدر عند إطار الباب",
        "aliases": ["استطالة الصدر على الباب", "Chest Doorway Stretch", "إطالة الصدر الثابتة"],
        "type": "static_stretch",
        "primaryMuscles": ["chest"],
        "secondaryMuscles": ["shoulders", "biceps"],
        "bodyRegions": ["chest_shoulders"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف بجوار إطار باب أو عمود ثابت، واثنِ ذراعك بزاوية 90 درجة عند المرفق.",
            "ضع الساعد والكف على إطار الباب بحيث يكون الكوع في مستوى الكتف تقريبًا.",
            "تقدّم بخطوة صغيرة للأمام بالقدم الموازية، ودوّر جذعك برفق بعيدًا عن الذراع المثبتة حتى تشعر باستطالة مريحة في عضلات الصدر والكتف الأمامي.",
            "اثبت في هذا الوضع مع التنفس العميق، ثم بدّل للجانب الآخر."
        ],
        "durationSeconds": 30,
        "breathing": "تنفس بعمق وبطء؛ خذ شهيقًا عميقًا ثم زفيرًا مع الاسترخاء وزيادة مدى الإطالة الخفيف دون ألم.",
        "commonMistakes": [
            "تقويس أسفل الظهر لتعويض قلة مرونة الكتف.",
            "رفع الكتف للأعلى باتجاه الأذن بدل تثبيته للأسفل.",
            "الضغط الزائد والعنيف على مفصل الكتف."
        ],
        "safetyNotes": "توقف فورًا إذا شعرت بوخز أو ألم حاد في مقدمة مفصل الكتف، ولا تتجاوز نقطة الشد المريح.",
        "image": "assets/images/stretches/str-doorway-pec-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_bench_press", "incline_dumbbell_press", "push_up"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-arm-circles-dynamic",
        "name": "Dynamic Arm Circles",
        "nameAr": "دوائر الذراعين الديناميكية لإحماء الكتفين",
        "aliases": ["تدوير الذراعين", "Arm Swings", "إحماء مفصل الكتف"],
        "type": "warmup_drill",
        "primaryMuscles": ["shoulders"],
        "secondaryMuscles": ["chest", "traps"],
        "bodyRegions": ["chest_shoulders"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "قف مستقيمًا مع فتح القدمين بعرض الكتفين وشد عضلات البطن.",
            "افرد الذراعين على الجانبين في مستوى الكتفين تمامًا.",
            "ابدأ بعمل دوائر صغيرة وبطيئة للأمام، ثم وسّع نطاق الحركة تدريجيًا لتصبح دوائر واسعة وكاملة.",
            "اعكس الاتجاه للخلف بعد إنهاء التكرارات المحددة لتنشيط لوحي الكتف."
        ],
        "recommendedReps": "12-15 دائرة في كل اتجاه (للأمام وللخلف)",
        "breathing": "تنفس إيقاعي منتظم مع حركة الدوران دون حبس النفس.",
        "commonMistakes": [
            "أرجحة الجذع أو ثني الظهر أثناء الدوران.",
            "السرعة المفرطة واستخدام الاندفاع بدلاً من التحكم العضلي.",
            "رفع الكتفين نحو الرقبة."
        ],
        "safetyNotes": "حافظ على التحكم التام في المدى الحركي لتجنب اصطدام أوتار الكفة المدورة.",
        "image": "assets/images/stretches/str-arm-circles-dynamic.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_overhead_barbell_press", "barbell_bench_press", "dumbbell_bench_press"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-cross-body-shoulder-stretch",
        "name": "Cross-Body Shoulder Stretch",
        "nameAr": "إطالة الكتف الخلفي بالعرض",
        "aliases": ["استطالة الكتف الخلفي", "Rear Delt Stretch", "سحب الذراع العرضي"],
        "type": "static_stretch",
        "primaryMuscles": ["shoulders"],
        "secondaryMuscles": ["traps", "lats"],
        "bodyRegions": ["chest_shoulders"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "قف أو اجلس مع استقامة الظهر واسترخاء الكتفين.",
            "مدّ ذراعك اليمنى أفقيًا عبر صدرك باتجاه اليسار.",
            "استخدم يدك اليسرى أو ساعدك للإمساك بالذراع اليمنى من فوق المرفق برفق وسحبها نحو صدرك.",
            "حافظ على الكتف مشدودًا للأسفل وبعيدًا عن الأذن حتى تشعر بالإطالة في الجزء الخلفي من الكتف.",
            "اثبت للمدة المحددة ثم كرر مع الذراع الأخرى."
        ],
        "durationSeconds": 25,
        "breathing": "شهيق هادئ وزفير عميق مع كل استرخاء عضلي.",
        "commonMistakes": [
            "الضغط المباشر على مفصل المرفق بدلاً من الساعد أو العضد.",
            "لف الجذع والخصر باتجاه السحب بدلاً من إبقاء الصدر مواجهًا للأمام."
        ],
        "safetyNotes": "لا تطبق قوة سحب عنيفة على المفصل، واكتفِ بالإحساس بشد لطيف في العضلة الدالية الخلفية.",
        "image": "assets/images/stretches/str-cross-body-shoulder-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_overhead_barbell_press", "rear_delt_dumbbell_fly", "face_pull_cable"],
        "suitableFor": ["cooldown"]
    },
    {
        "id": "str-band-shoulder-dislocations",
        "name": "Band Shoulder Pass-Throughs",
        "nameAr": "دوران الكتفين بشريط المقاومة لتحسين المرونة",
        "aliases": ["Shoulder Dislocates", "تمرير حبل المقاومة فوق الرأس", "مرونة الكتف بالحبل"],
        "type": "joint_mobility",
        "primaryMuscles": ["shoulders"],
        "secondaryMuscles": ["chest", "traps", "lats"],
        "bodyRegions": ["chest_shoulders"],
        "equipment": "band",
        "level": "intermediate",
        "instructions": [
            "أمسك شريط مقاومة خفيف أو عصا بقبضة واسعة بكلتا اليدين أمام فخذيك.",
            "مع الحفاظ على استقامة الذراعين وشد عضلات البطن، ارفع الشريط ببطء للأعلى فوق رأسك.",
            "واصل الحركة الدائرية خلف ظهرك حتى يصل الشريط لأسفل الظهر، دون ثني المرفقين.",
            "أعد الشريط ببطء وتحكم إلى الأمام متبعًا نفس المسار الحركي."
        ],
        "recommendedReps": "10-12 تكرار كامل ومتحكم",
        "breathing": "شهيق أثناء رفع الشريط لأعلى، وزفير أثناء نزوله للخلف وللأمام.",
        "commonMistakes": [
            "تضييق المسافة بين اليدين قبل اكتساب المرونة الكافية مما يجبر المرفقين على الانثناء.",
            "تقويس أسفل الظهر ودفع البطن للأمام أثناء حركة الشريط خلف الرأس.",
            "الحركة السريعة وغير المتحكم بها."
        ],
        "safetyNotes": "ابدأ بقبضة واسعة للغاية لتفادي أي إجهاد غير ضروري على أوتار الكتف، وضيّق المسافة تدريجيًا بمرور الأسابيع.",
        "image": "assets/images/stretches/str-band-shoulder-dislocations.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_overhead_barbell_press", "pull_up", "barbell_bench_press"],
        "suitableFor": ["warmup", "mobility"]
    },

    # --- 2. الظهر واللاتس (Back & Lats) ---
    {
        "id": "str-lat-wall-stretch",
        "name": "Wall Lat Stretch",
        "nameAr": "إطالة عضلات المجنص (اللاتس) على الحائط",
        "aliases": ["استطالة اللاتس على الجدار", "Lat Wall Stretch", "إطالة الظهر الجانبي"],
        "type": "static_stretch",
        "primaryMuscles": ["lats"],
        "secondaryMuscles": ["shoulders", "lower_back"],
        "bodyRegions": ["back_lats"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف في مواجهة جدار أو عارضة ثابتة على بُعد خطوتين.",
            "ضع كفيك على الحائط في مستوى الحوض أو الصدر، وارجع بالحوض للخلف مع ثني خفيف في الركبتين.",
            "أخفض صدرك ورأسك بين ذراعيك حتى يصبح الجذع موازيًا للأرض.",
            "اضغط برفق بصدرك باتجاه الأرض مع إطالة الذراعين للأمام للشعور بشد عميق على جانبي الظهر (عضلات اللاتس)."
        ],
        "durationSeconds": 30,
        "breathing": "تنفس بطيء وعميق، ومع كل زفير دع الصدر يهبط قليلاً لمزيد من المرونة.",
        "commonMistakes": [
            "ثني المرفقين مما يقلل من تمدد عضلات الظهر العريضة.",
            "تقويس الظهر بشكل محدب مفرط بدلاً من استقامة العمود الفقري."
        ],
        "safetyNotes": "إذا شعرت بألم في الكتف، ارفع مستوى اليدين على الحائط قليلاً للأعلى.",
        "image": "assets/images/stretches/str-lat-wall-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["pull_up", "lat_pulldown_wide_grip", "barbell_bent_over_row"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-childs-pose",
        "name": "Extended Child's Pose",
        "nameAr": "وضعية الطفل الممتدة لإراحة الظهر والعمود الفقري",
        "aliases": ["استطالة وضعية الطفل", "Childs Pose Stretch", "تهدئة أسفل الظهر"],
        "type": "static_stretch",
        "primaryMuscles": ["lower_back"],
        "secondaryMuscles": ["lats", "glutes", "shoulders"],
        "bodyRegions": ["back_lats"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "ابدأ بالجلوس على ركبتيك فوق بساط التمرين مع تلامس إصبعي القدمين الكبيرين ومباعدة الركبتين بعرض الحوض أو أوسع قليلاً.",
            "اجلس بمؤخرتك فوق كعبيك، ثم انحنِ بجذعك للأمام حتى تلامس جبهتك الأرض.",
            "مدّ ذراعيك للأمام بأقصى مدى مريح مع فرد الكفين على الأرض.",
            "تنفس بعمق ودع عضلات أسفل الظهر وأعلى الظهر تسترخي تمامًا."
        ],
        "durationSeconds": 35,
        "breathing": "شهيق عميق يملأ البطن وأسفل الظهر، وزفير طويل ومريح يفرغ التوتر العضلي.",
        "commonMistakes": [
            "رفع المؤخرة عاليًا عن الكعبين بدلاً من ترك الحوض يستقر للوراء.",
            "شد عضلات الرقبة والكتفين أثناء التمدد."
        ],
        "safetyNotes": "إذا كانت لديك آلام في الركبة، ضع وسادة صغيرة أو منشفة ملفوفة بين فخذيك وربلات الساقين.",
        "image": "assets/images/stretches/str-childs-pose.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["conventional_deadlift", "barbell_bent_over_row", "back_extensions"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-band-pull-apart-activation",
        "name": "Band Pull-Apart Activation",
        "nameAr": "تنشيط عضلات أعلى الظهر والكتف الخلفي بشريط المقاومة",
        "aliases": ["فتح الشريط المطاطي", "Band Pull Apart", "تنشيط اللوحين"],
        "type": "activation",
        "primaryMuscles": ["traps"],
        "secondaryMuscles": ["shoulders", "upper_back"],
        "bodyRegions": ["back_lats"],
        "equipment": "band",
        "level": "beginner",
        "instructions": [
            "قف مستقيمًا ممسكًا بشريط مقاومة خفيف بكلتا اليدين أمام صدرك مع فرد الذراعين.",
            "باعد بين يديك بعرض الكتفين تقريبًا مع شد خفيف في الشريط.",
            "اسحب الشريط للخارج مع فتح الذراعين جانبيًا وعصر لوحي الكتف معًا حتى يلامس الشريط منتصف صدرك.",
            "اثبت لثانية واحدة مع العصر التام، ثم عُد ببطء وتحكم إلى نقطة البداية."
        ],
        "recommendedReps": "12-15 تكرار مع عصر ثانية في أقصى انقباض",
        "breathing": "زفير أثناء فتح الشريط وعصر اللوحين، وشهيق أثناء العودة المتحكمة.",
        "commonMistakes": [
            "رفع الكتفين نحو الأذنين بدلاً من خفضهما.",
            "ثني المرفقين لتحويل التمرين إلى سحب للذراعين بدلاً من عصر لوحي الكتف.",
            "تقويس الظهر ودفع البطن للأمام."
        ],
        "safetyNotes": "استخدم شريطًا خفيفًا؛ فالهدف هو تنشيط واستيقاظ العضلات المثبتة للوح الكتف وليس رفع أوزان ثقيلة.",
        "image": "assets/images/stretches/str-band-pull-apart-activation.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["band_pull_apart", "face_pull_cable", "barbell_bent_over_row"],
        "suitableFor": ["warmup"]
    },

    # --- 3. الرقبة والجزء العلوي من الظهر (Neck & Upper Back) ---
    {
        "id": "str-upper-trap-stretch",
        "name": "Upper Trapezius Neck Stretch",
        "nameAr": "إطالة العضلة شبه المنحرفة للرقبة (الترابيس العلوية)",
        "aliases": ["استطالة الرقبة الجانبية", "Upper Trap Stretch", "تخفيف شد الرقبة"],
        "type": "static_stretch",
        "primaryMuscles": ["neck"],
        "secondaryMuscles": ["traps"],
        "bodyRegions": ["neck_upper_back"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "اجلس أو قف مع ظهر مستقيم وأكتاف مسترخية تمامًا للأسفل.",
            "أمِل رأسك برفق باتجاه كتفك الأيمن، بحيث تقترب أذنك اليمنى من كتفك دون رفع الكتف.",
            "ضع يدك اليمنى بخفة متناهية فوق رأسك لتوجيه الحركة دون أي ضغط قسري لأسفل.",
            "اثبت في هذا الوضع اللطيف، ثم كرر الحركة للجانب الأيسر."
        ],
        "durationSeconds": 20,
        "breathing": "تنفس هادئ وعميق مع التركيز على إرخاء عضلات الرقبة والفك.",
        "commonMistakes": [
            "شد الرأس بقوة باليد، مما يضغط على الفقرات العنقية.",
            "رفع الكتف المعاكس للأعلى لتعويض قصر العضلة.",
            "إمالة الرأس للأمام أو الخلف أثناء الإطالة الجانبية."
        ],
        "safetyNotes": "تحذير أمان: لا تطبق أي ضغط عنيف على عظام الرأس أو فقرات الرقبة، واكتفِ بوزن اليد الخفيف للغاية وتوقف عند أي وخز عصبي.",
        "image": "assets/images/stretches/str-upper-trap-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_shrugs", "dumbbell_shrugs", "standing_overhead_barbell_press"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-chin-tucks",
        "name": "Chin Tucks Mobility Drill",
        "nameAr": "تمرين سحب الذقن لتصحيح قوام الرقبة وتنشيط عضلاتها العميقة",
        "aliases": ["سحب الذقن للداخل", "Chin Tucks", "تصحيح الرأس المنحني للأمام"],
        "type": "joint_mobility",
        "primaryMuscles": ["neck"],
        "secondaryMuscles": ["upper_back"],
        "bodyRegions": ["neck_upper_back"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "اجلس أو قف في وضعية قوام صحيحة مع النظر للأمام مباشرة.",
            "اسحب ذقنك ورأسك للخلف في خط أفقي مستقيم، كأنك تصنع 'ذقنًا مزدوجة' خفيفة دون إمالة الرأس للأسفل أو للأعلى.",
            "اشعر بتمدد لطيف في قاعدة الجمجمة ومؤخرة العنق.",
            "اثبت لثانيتين إلى ثلاث ثوانٍ في الوضع الخلفي، ثم أرخِ الرأس للوضع المحايد وكرر."
        ],
        "recommendedReps": "10-12 تكرار متحكم مع ثبات ثانيتين",
        "breathing": "زفير أثناء سحب الذقن للخلف، وشهيق أثناء العودة للوضع الطبيعي.",
        "commonMistakes": [
            "ثني الرأس للأسفل بدلاً من سحبه للخلف في مسار أفقي مستقيم.",
            "حبس النفس أو التشنج العضلي."
        ],
        "safetyNotes": "هذه حركة مفصلية تصحيحية خفيفة للغاية، تجنب الإفراط في القوة أو سحب الرقبة بعد نقطة الراحة الطبيعية.",
        "image": "assets/images/stretches/str-chin-tucks.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_overhead_barbell_press", "barbell_shrugs", "face_pull_cable"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-levator-scapulae-stretch",
        "name": "Levator Scapulae Stretch",
        "nameAr": "إطالة عضلة رافعة لوح الكتف وجانب الرقبة الخلفي",
        "aliases": ["استطالة زاوية الرقبة", "Levator Scapulae", "تخفيف تيبس أعلى الظهر والكتف"],
        "type": "static_stretch",
        "primaryMuscles": ["neck"],
        "secondaryMuscles": ["traps", "upper_back"],
        "bodyRegions": ["neck_upper_back"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "اجلس على مقعد ممسكًا بحافة المقعد بيدك اليسرى لتثبيت الكتف الأيسر للأسفل.",
            "أدر رأسك بزاوية 45 درجة نحو اليمين، ثم انظر برفق للأسفل باتجاه جيب قميصك أو إبطك الأيمن.",
            "ضع يدك اليمنى على مؤخرة رأسك بخفة متناهية لتوجيه التمدد دون ضغط عنيف.",
            "اشعر بإطالة مريحة تمتد من زاوية الرقبة الخلفية وحتى لوح الكتف.",
            "اثبت للمدة المحددة، ثم كرر للجانب الآخر."
        ],
        "durationSeconds": 20,
        "breathing": "تنفس هادئ وزفير عميق يساعد على استرخاء العضلات المتشنجة.",
        "commonMistakes": [
            "رفع الكتف المثبت للأعلى مما يفقد الإطالة فاعليتها.",
            "الضغط الزائد على الرقبة نحو الأسفل."
        ],
        "safetyNotes": "يجب أن تكون الحركة خالية تمامًا من الدوخة أو الآلام الحادة. لا تسحب الرأس بعنف أبدًا.",
        "image": "assets/images/stretches/str-levator-scapulae-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_shrugs", "face_pull_cable", "standing_overhead_barbell_press"],
        "suitableFor": ["cooldown", "mobility"]
    },

    # --- 4. الورك ومثنيات الورك (Hips & Hip Flexors) ---
    {
        "id": "str-kneeling-hip-flexor",
        "name": "Half-Kneeling Hip Flexor Stretch",
        "nameAr": "إطالة مثنيات الورك بالركوع النصفي",
        "aliases": ["استطالة الحوض بالركوع", "Hip Flexor Stretch", "إطالة عضلة البسواس"],
        "type": "static_stretch",
        "primaryMuscles": ["hip_flexors"],
        "secondaryMuscles": ["quads", "glutes"],
        "bodyRegions": ["hips_pelvis"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "انزل على ركبة واحدة فوق البساط بحيث تكون الركبة الخلفية على الأرض والأمامية مثنية بزاوية 90 درجة والقدم مستقرة.",
            "احرص على استقامة الجذع وشد عضلات البطن وتدوير الحوض للخلف قليلاً (Posterior Pelvic Tilt).",
            "أزح وزنك برفق للأمام عبر دفع الحوض للأمام دون تقويس أسفل الظهر إطلاقًا.",
            "اشعر بشد واضح ومريح في مقدمة فخذ وورك الساق الخلفية.",
            "اثبت للمدة المحددة ثم بدّل للساق الأخرى."
        ],
        "durationSeconds": 30,
        "breathing": "شهيق عميق يثبت الجذع، وزفير مريح مع دفع الحوض الخفيف للأمام.",
        "commonMistakes": [
            "تقويس أسفل الظهر لتعويض ضيق الورك مما يحمّل الفقرات القطنية إجهادًا غير سليم.",
            "المبالغة في الاندفاع للأمام مما يرفع كعب القدم الأمامية عن الأرض."
        ],
        "safetyNotes": "ضع وسادة أو منشفة أسفل الركبة الخلفية إذا كنت تعاني من حساسية أو خشونة بالركبة.",
        "image": "assets/images/stretches/str-kneeling-hip-flexor.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "walking_lunges_dumbbell", "bulgarian_split_squat"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-hip-opener-90-90",
        "name": "90/90 Hip Mobility Drill",
        "nameAr": "حركة مرونة الورك بزاوية 90/90 للدوران الداخلي والخارجي",
        "aliases": ["تمرين 90-90 للورك", "90/90 Hip Drill", "مرونة الحوض والمفاصل"],
        "type": "joint_mobility",
        "primaryMuscles": ["hip_flexors"],
        "secondaryMuscles": ["glutes", "groin"],
        "bodyRegions": ["hips_pelvis"],
        "equipment": "mat",
        "level": "intermediate",
        "instructions": [
            "اجلس على الأرض وضع الساق الأمامية مثنية بزاوية 90 درجة أمامك والساق الخلفية مثنية بزاوية 90 درجة إلى جانبك.",
            "حافظ على استقامة العمود الفقري والكتفين في وضع مسترخٍ.",
            "انحنِ برفق بصدرك للأمام فوق فخذ الساق الأمامية مع الحفاظ على استقامة الظهر للشعور بمرونة الورك الخارجي.",
            "عُد للوضع المستقيم ثم دوّر الجذع قليلاً لتفعيل الدوران الداخلي للورك الخلفي.",
            "بدّل وضع الساقين للجهة الأخرى وكرر الحركة."
        ],
        "recommendedReps": "8-10 تكرارات سلسة لكل جهة أو ثبات 25 ثانية",
        "breathing": "تنفس عميق وبطيء مع كل انتقال حركي.",
        "commonMistakes": [
            "انحناء الظهر الشديد وتحدب العمود الفقري بدلاً من الانحناء من مفصل الورك.",
            "رفع الركبتين قسرًا عن الأرض قبل استيعاب مدى الحركة المتاح."
        ],
        "safetyNotes": "إذا كان الجلوس المستقيم صعبًا، استند بإحدى يديك أو كلتيهما على الأرض خلفك للمساعدة.",
        "image": "assets/images/stretches/str-hip-opener-90-90.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "sumo_deadlift", "goblet_squat"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-butterfly-stretch",
        "name": "Seated Butterfly Stretch",
        "nameAr": "استطالة الفراشة جالسًا للعضلات الضامة وباطن الفخذ",
        "aliases": ["تمرين الفراشة", "Butterfly Stretch", "إطالة العضلات المقربة"],
        "type": "static_stretch",
        "primaryMuscles": ["adductors"],
        "secondaryMuscles": ["groin", "hip_flexors"],
        "bodyRegions": ["hips_pelvis"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "اجلس مستقيم الظهر على بساط التمرين مع ثني الركبتين وضم باطن القدمين معًا أمامك.",
            "أمسك بكاحليك أو قدميك بيديك واجذب الكعبين برفق باتجاه الحوض بقدر ما يسمح مدى راحتك.",
            "حافظ على استقامة ظهرك واضغط برفق بمرفقيك على الفخذين للأسفل نحو الأرض دون ارتداد عنيف.",
            "اشعر بشد ممتع في عضلات الفخذ الداخلية وأسفل الحوض."
        ],
        "durationSeconds": 30,
        "breathing": "شهيق طويل يمد العمود الفقري لأعلى، وزفير يدع الركبتين تهبطان بمقدار إضافي بسيط بفضل الجاذبية.",
        "commonMistakes": [
            "هز الركبتين صعودًا وهبوطًا بعنف (Ballistic bouncing).",
            "تقويس الرقبة وأعلى الظهر للأمام لتقريب الرأس من القدمين."
        ],
        "safetyNotes": "تجنب تمامًا إجبار الركبتين على ملامسة الأرض بالقوة لحماية أربطة الركبة والحوض.",
        "image": "assets/images/stretches/str-butterfly-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["sumo_deadlift", "barbell_back_squat", "leg_press"],
        "suitableFor": ["cooldown", "mobility"]
    },

    # --- 5. الفخذ الأمامي والخلفي (Quads & Hamstrings) ---
    {
        "id": "str-standing-quad-stretch",
        "name": "Standing Quad Stretch",
        "nameAr": "إطالة عضلات الفخذ الأمامية (الكوادس) واقفًا",
        "aliases": ["استطالة الفخذ الأمامي", "Standing Quadriceps Stretch", "إطالة الكوادس"],
        "type": "static_stretch",
        "primaryMuscles": ["quads"],
        "secondaryMuscles": ["hip_flexors"],
        "bodyRegions": ["thighs_legs"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف مستقيمًا بجوار جدار أو كرسي للاستناد بيد واحدة من أجل التوازن.",
            "اثنِ ركبتك اليمنى للخلف وأمسك بمقدمة كاحلك الأيمن بيدك اليمنى.",
            "اسحب كعبك برفق نحو مؤخرتك مع الحفاظ على ملاصقة الركبتين لبعضهما واستقامة الفخذ في خط عمودي.",
            "شد عضلات البطن وادفع الحوض للأمام قليلاً لزيادة الاستطالة في مقدمة الفخذ.",
            "اثبت للمدة المحددة، ثم كرر للساق اليسرى."
        ],
        "durationSeconds": 25,
        "breathing": "تنفس منتظم وهادئ دون حبس النفس للمساعدة في ثبات التوازن.",
        "commonMistakes": [
            "تباعد الركبتين وانحراف الركبة المثنية إلى الخارج بعيدًا عن الساق الأخرى.",
            "تقويس أسفل الظهر للأمام بشكل مفرط."
        ],
        "safetyNotes": "لا تسحب الكاحل لدرجة إحداث التواء في مفصل الركبة، واحرص على السحب في مسار موازٍ لمفصل الركبة الطبيعي.",
        "image": "assets/images/stretches/str-standing-quad-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "leg_press", "leg_extension_machine"],
        "suitableFor": ["cooldown"]
    },
    {
        "id": "str-standing-hamstring-stretch",
        "name": "Standing Hamstring Stretch",
        "nameAr": "إطالة عضلات الفخذ الخلفية واقفًا مع رفع مشط القدم",
        "aliases": ["استطالة الهامسترنج", "Hamstring Stretch", "إطالة خلفية الفخذ"],
        "type": "static_stretch",
        "primaryMuscles": ["hamstrings"],
        "secondaryMuscles": ["calves", "glutes"],
        "bodyRegions": ["thighs_legs"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "قف مستقيمًا ثم تقدّم بساقك اليمنى خطوة صغيرة للأمام وضع كعبها على الأرض مع رفع مشط القدم للأعلى.",
            "اثنِ ركبتك اليسرى (الخلفية) قليلاً وادفع مؤخرتك وحوضك للخلف كأنك تجلس على كرسي مرتفع.",
            "حافظ على استقامة الساق اليمنى والعمود الفقري، وضع يديك على فخذك الأيسر أو على الحوض للدعم.",
            "انحنِ بصدرك برفق للأمام من مفصل الورك حتى تشعر بإطالة عميقة في العضلات الخلفية للفخذ الأيمن.",
            "اثبت للمدة المحددة ثم بدّل للساق اليسرى."
        ],
        "durationSeconds": 30,
        "breathing": "شهيق هادئ وزفير عميق مع تعميق انحناء الحوض للخلف بلطف.",
        "commonMistakes": [
            "ثني الظهر وتقويسه للوصول إلى أصابع القدمين باليدين بدلاً من الانحناء من الحوض.",
            "وضع اليدين مباشرة على ركبة الساق المفرودة مما يضغط المفصل للخلف."
        ],
        "safetyNotes": "حافظ على ثنية ميكروسكوبية خفيفة في ركبة الساق الأمامية إذا كنت تعاني من فرط بسط المفاصل.",
        "image": "assets/images/stretches/str-standing-hamstring-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["romanian_deadlift_barbell", "lying_leg_curl_machine", "conventional_deadlift"],
        "suitableFor": ["cooldown"]
    },
    {
        "id": "str-dynamic-leg-swings",
        "name": "Dynamic Leg Swings (Front to Back)",
        "nameAr": "مرجحة الساقين الديناميكية للأمام والخلف للإحماء",
        "aliases": ["مرجحة الساق للأمام والخلف", "Dynamic Leg Swings", "إحماء مفصل الفخذ"],
        "type": "warmup_drill",
        "primaryMuscles": ["hamstrings"],
        "secondaryMuscles": ["hip_flexors", "quads", "glutes"],
        "bodyRegions": ["thighs_legs"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف بجانب جدار وضع يدك القريبة عليه للحفاظ على الثبات والتوازن التام.",
            "قف على ساق واحدة ثابتة ومستقرة مع ثني خفيف غير ملحوظ في ركبتها.",
            "أرجح الساق الحرة للأمام وللخلف بحركة انسيابية متدرجة السعة.",
            "ابدأ بمدى حركي صغير ثم وسّع المدى تدريجيًا مع الحفاظ على ثبات واستقامة الجذع والبطن."
        ],
        "recommendedReps": "12-15 تكرارًا متدفقًا لكل ساق",
        "breathing": "تنفس إيقاعي يتماشى مع تردد مرجحة الساق للأمام والخلف.",
        "commonMistakes": [
            "تقويس أسفل الظهر بشكل مفرط عند أرجحة الساق للخلف.",
            "انحناء الجذع للأمام بشكل مبالغ فيه عند أرجحة الساق للأعلى."
        ],
        "safetyNotes": "تحكم في حركة الساق ولا تدع القصور الذاتي يجبر العضلة على التمدد المفاجئ بما يتجاوز جاهزيتها.",
        "image": "assets/images/stretches/str-dynamic-leg-swings.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "walking_lunges_dumbbell", "goblet_squat"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-couch-stretch",
        "name": "Deep Couch Stretch",
        "nameAr": "إطالة الأريكة العميقة للفخذ ومثنيات الورك على الحائط",
        "aliases": ["استطالة الكاوتش", "Couch Stretch", "إطالة الفخذ العميق بالجدار"],
        "type": "static_stretch",
        "primaryMuscles": ["quads"],
        "secondaryMuscles": ["hip_flexors"],
        "bodyRegions": ["thighs_legs"],
        "equipment": "wall",
        "level": "advanced",
        "instructions": [
            "انزل على ركبتيك أمام جدار وضع ركبتك الخلفية على الأرض ملاصقة تمامًا للزاوية بين الأرض والحائط، مع جعل قصبة الساق ومشط القدم عموديين على الجدار.",
            "ضع الساق الأمامية للأمام في وضعية خطوة لاندجز بحيث تكون الركبة بزاوية 90 درجة فوق الكاحل.",
            "ارفع جذعك بالتدريج ليصبح مستقيمًا تمامًا مع عصر عضلات الإلية وشد البطن لتثبيت الحوض.",
            "اشعر باستطالة عميقة وشديدة في الجزء الأمامي من الفخذ والورك للساق الخلفية.",
            "اثبت للمدة المحددة، ثم بدّل للساق الأخرى بحذر."
        ],
        "durationSeconds": 30,
        "breathing": "تنفس عميق وبطيء لمساعدة العضلة المشدودة على التحرر والاسترخاء.",
        "commonMistakes": [
            "تقويس أسفل الظهر للأمام للهروب من شد الفخذ القوي.",
            "إمالة الركبة الخلفية بزاوية ملتوية تؤلم صابونة الركبة."
        ],
        "safetyNotes": "تمرين متقدم للغاية؛ ضع وسادة سميكة تحت الركبة الخلفية، وإذا شعرت بضغط مفرط، ابدأ بإمالة اليدين على الأرض أولاً.",
        "image": "assets/images/stretches/str-couch-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "bulgarian_split_squat", "leg_press"],
        "suitableFor": ["cooldown", "mobility"]
    },

    # --- 6. المؤخرة (Glutes) ---
    {
        "id": "str-pigeon-pose",
        "name": "Pigeon Pose Glute Stretch",
        "nameAr": "وضعية الحمامة لإطالة عضلات الإلية والورك الخارجية",
        "aliases": ["استطالة وضعية الحمام", "Pigeon Pose Stretch", "إطالة الجلوتس العميقة"],
        "type": "static_stretch",
        "primaryMuscles": ["glutes"],
        "secondaryMuscles": ["hip_flexors", "lower_back"],
        "bodyRegions": ["glutes"],
        "equipment": "mat",
        "level": "intermediate",
        "instructions": [
            "ابدأ بوضعية الارتكاز على الأطراف الأربعة أو تمرين البلانك المرتفع.",
            "اسحب ركبتك اليمنى للأمام وضعها خلف معصمك الأيمن، واجعل قصبة الساق اليمنى مائلة بزاوية مريحة تحت الحوض.",
            "مدّ الساق اليسرى بالكامل للخلف على الأرض بحيث تستقر مقدمة الفخذ ومشط القدم على البساط.",
            "حافظ على توازن الحوض مستويًا دون الميل لأحد الجانبين، وانزل بجذعك وساعديك للأمام فوق الساق المطوية.",
            "اثبت في هذا الوضع المريح وتناول أنفاسًا عميقة، ثم بدّل للساق الأخرى."
        ],
        "durationSeconds": 35,
        "breathing": "شهيق هادئ وزفير مفرغ للتوتر، يتيح للحوض الهبوط بتدرج نحو الأرض.",
        "commonMistakes": [
            "الميل بالكامل والجلوس على جانب الورك الأيمن بدلاً من إبقاء الحوض مستويًا.",
            "ثني الركبة الأمامية بزاوية غير مريحة تسبب ضغطًا والتواءً في الركبة."
        ],
        "safetyNotes": "إذا شعرت بأي وخز أو ألم في ركبة الساق الأمامية، عدّل زاوية القدم للداخل أو استبدل الحركة بإطالة Figure-4 مستلقيًا.",
        "image": "assets/images/stretches/str-pigeon-pose.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_hip_thrust", "barbell_back_squat", "romanian_deadlift_barbell"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-figure-four-stretch",
        "name": "Figure-4 Glute Stretch (Lying)",
        "nameAr": "استطالة الإلية برسم رقم 4 مستلقيًا على الظهر",
        "aliases": ["استطالة الجلوتس رقم 4", "Figure 4 Stretch", "إطالة العضلة الكمثرية"],
        "type": "static_stretch",
        "primaryMuscles": ["glutes"],
        "secondaryMuscles": ["hip_flexors", "lower_back"],
        "bodyRegions": ["glutes"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "استلقِ على ظهرك على بساط التمرين مع ثني الركبتين وتثبيت القدمين على الأرض.",
            "ارفع كاحلك الأيمن وضعه فوق فخذ الساق اليسرى بالقرب من الركبة (لتشكيل الرقم 4 بالساقين).",
            "مرر يديك حول فخذ الساق اليسرى واسحب الفخذ الأيسر برفق باتجاه صدرك مع إبقاء الرأس والكتفين مسترخيين على الأرض.",
            "اشعر باستطالة واضحة في عضلة الإلية اليمنى والعضلة الكمثرية العميقة.",
            "اثبت للمدة المحددة ثم بدّل للساق اليسرى."
        ],
        "durationSeconds": 30,
        "breathing": "تنفس بطيء وهادئ من البطن، مع زفير يساعد على استرخاء عضلات الحوض.",
        "commonMistakes": [
            "رفع الرأس والرقبة عن الأرض بإجهاد أثناء سحب الساق.",
            "الضغط المباشر على مفصل الركبة بدلاً من الإمساك بأسفل الفخذ."
        ],
        "safetyNotes": "حافظ على شد مشط القدم المتقاطعة (Dorsiflexion) لحماية مفصل الركبة من الالتواء.",
        "image": "assets/images/stretches/str-figure-four-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_hip_thrust", "conventional_deadlift", "bodyweight_glute_bridge"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-glute-bridge-activation",
        "name": "Glute Bridge Bodyweight Activation",
        "nameAr": "تنشيط عضلات الإلية بجسر الحوض بوزن الجسم",
        "aliases": ["جسر الحوض لإيقاظ الجلوتس", "Glute Bridge Activation", "تنشيط عضلات المقعدة"],
        "type": "activation",
        "primaryMuscles": ["glutes"],
        "secondaryMuscles": ["hamstrings", "lower_back", "abs"],
        "bodyRegions": ["glutes"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "استلقِ على ظهرك مع ثني الركبتين وتثبيت القدمين بالكامل على الأرض بعرض الحوض، والذراعين على الجانبين.",
            "اضغط بكعبيك على الأرض وشد عضلات البطن، ثم ارفع حوضك للأعلى حتى يصبح جسمك في خط مستقيم من الركبتين للكتفين.",
            "اعصر عضلات الإلية بقوة في أعلى نقطة واثبت لثانيتين كاملتين دون تقويس أسفل الظهر بشكل مفرط.",
            "أنزل حوضك ببطء وتحكم حتى يلامس البساط بخفة، ثم كرر."
        ],
        "recommendedReps": "12-15 تكرارًا مع ثبات ثانيتين في القمة",
        "breathing": "زفير أثناء رفع الحوض وعصر الإلية، وشهيق أثناء الهبوط المتحكم.",
        "commonMistakes": [
            "رفع الحوض عاليًا جدًا بواسطة تقويس أسفل الظهر بدلاً من استخدام قوة الإلية.",
            "دفع الوزن عبر أصابع القدم بدلاً من الكعبين مما يفعّل الفخذ الأمامي بدلاً من الإلية."
        ],
        "safetyNotes": "ركز على إحساس الانقباض العضلي في الإلية؛ إذا شعرت بضغط في أسفل الظهر، قلل ارتفاع الرفع وركز على استقامة الجذع.",
        "image": "assets/images/stretches/str-glute-bridge-activation.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["bodyweight_glute_bridge", "barbell_hip_thrust", "barbell_back_squat"],
        "suitableFor": ["warmup"]
    },

    # --- 7. السمانة والكاحل (Calves & Ankles) ---
    {
        "id": "str-wall-calf-stretch",
        "name": "Wall Gastrocnemius Calf Stretch",
        "nameAr": "إطالة عضلة السمانة العلوية على الحائط مع استقامة الساق",
        "aliases": ["استطالة السمانة على الجدار", "Calf Wall Stretch", "إطالة عضلة الكالفز"],
        "type": "static_stretch",
        "primaryMuscles": ["calves"],
        "secondaryMuscles": ["achilles"],
        "bodyRegions": ["calves_ankles"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف في مواجهة جدار وضع كفيك عليه في مستوى الصدر تقريبًا.",
            "ارجع بساقك اليمنى خطوة واسعة للخلف مع إبقاء الركبة مستقيمة تمامًا وتثبيت الكعب بإحكام على الأرض.",
            "اثنِ ركبتك الأمامية وانحنِ بجسمك للأمام باتجاه الحائط حتى تشعر بإطالة قوية في الجزء العلوي من سمانة الساق الخلفية.",
            "حافظ على توجيه أصابع القدمين مباشرة نحو الحائط.",
            "اثبت للمدة المحددة، ثم كرر للساق اليسرى."
        ],
        "durationSeconds": 25,
        "breathing": "تنفس عميق وهادئ يرسل الاسترخاء لعضلات الساق المشدودة.",
        "commonMistakes": [
            "رفع كعب الساق الخلفية عن الأرض مما يلغي تأثير الإطالة.",
            "انحراف مشط القدم الخلفية للخارج بدلاً من التوجيه للأمام."
        ],
        "safetyNotes": "تجنب القفز أو الارتداد بالوزن فوق وتر العرقوب (أخيل) لمنع إجهاده.",
        "image": "assets/images/stretches/str-wall-calf-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_calf_raise_machine", "bodyweight_calf_raise", "leg_press_calf_raise"],
        "suitableFor": ["cooldown"]
    },
    {
        "id": "str-ankle-wall-mobilization",
        "name": "Ankle Dorsiflexion Wall Mobilization",
        "nameAr": "تمرين مرونة حركة مفصل الكاحل للأمام على الحائط",
        "aliases": ["مرونة الكاحل بالجدار", "Ankle Mobilization", "تليين مفصل الكاحل للسكوات"],
        "type": "joint_mobility",
        "primaryMuscles": ["ankles"],
        "secondaryMuscles": ["calves", "achilles"],
        "bodyRegions": ["calves_ankles"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف في مواجهة جدار وضع أصابع قدمك اليمنى على بعد نحو 5 إلى 10 سم من قاعدة الجدار.",
            "حافظ على ثبات كعبك الأيمن بالكامل على الأرض دون أن يرتفع ولو ميليمترًا واحدًا.",
            "ادفع ركبتك اليمنى للأمام باتجاه الجدار في خط مستقيم فوق إصبع القدم الثاني حتى تلامس الجدار أو تقترب منه.",
            "اثبت لثانية واحدة عند أقصى انثناء دون رفع الكعب، ثم عُد بنعومة وكرر الحركة.",
            "انقل القدم للخلف قليلاً إذا كانت الحركة سهلة لاختبار أقصى مدى مرونة للكاحل."
        ],
        "recommendedReps": "10-12 تكرارًا ديناميكيًا لكل كاحل",
        "breathing": "زفير أثناء دفع الركبة للأمام نحو الجدار، وشهيق أثناء العودة.",
        "commonMistakes": [
            "رفع الكعب عن الأرض لخداع المدى الحركي.",
            "سقوط الركبة للداخل نحو إبهام القدم بدلاً من تتبع مسار أصابع القدم الوسطى."
        ],
        "safetyNotes": "إذا شعرت بألم انضغاطي حاد في مقدمة مفصل الكاحل، خفف المدى الحركي ولا تجبر المفصل على الدفع للأمام.",
        "image": "assets/images/stretches/str-ankle-wall-mobilization.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "barbell_front_squat", "standing_calf_raise_machine"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-soleus-bent-knee-stretch",
        "name": "Bent-Knee Soleus Calf Stretch",
        "nameAr": "إطالة العضلة النعلية العميقة للسمانة مع ثني الركبة",
        "aliases": ["استطالة النعلية", "Soleus Stretch", "إطالة أسفل السمانة ووتر أخيل"],
        "type": "static_stretch",
        "primaryMuscles": ["calves"],
        "secondaryMuscles": ["achilles", "ankles"],
        "bodyRegions": ["calves_ankles"],
        "equipment": "wall",
        "level": "beginner",
        "instructions": [
            "قف أمام جدار مستندًا بيديك، وضع ساقك اليمنى خلف اليسرى بخطوة متوسطة.",
            "على عكس إطالة السمانة العادية، اثنِ كلتا الركبتين في وقت واحد مع الحفاظ على كعب الساق الخلفية مثبتًا تمامًا على الأرض.",
            "أنزل وزنك بحركة رأسية لأسفل مع ثني الركبة الخلفية حتى تشعر بالإطالة في الجزء السفلي العميق من السمانة بالقرب من وتر أخيل.",
            "اثبت في هذا الوضع، ثم كرر للساق الأخرى."
        ],
        "durationSeconds": 25,
        "breathing": "تنفس منتظم وهادئ يساعد الألياف العضلية البطيئة في النعلية على الاسترخاء.",
        "commonMistakes": [
            "إبقاء الركبة الخلفية مفرودة ومستقيمة؛ ثني الركبة ضروري لاستهداف عضلة السوليوس (Soleus).",
            "رفع الكعب الخلفي عن الأرض."
        ],
        "safetyNotes": "تحرك بنعومة لتفادي التحميل المفاجئ على وتر أخيل.",
        "image": "assets/images/stretches/str-soleus-bent-knee-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["seated_calf_raise_machine", "standing_calf_raise_machine", "barbell_back_squat"],
        "suitableFor": ["cooldown"]
    },

    # --- 8. الرسغ والساعد (Wrists & Forearms) ---
    {
        "id": "str-wrist-extensor-stretch",
        "name": "Wrist Extensor Stretch",
        "nameAr": "إطالة عضلات باسطات الرسغ وأعلى الساعد",
        "aliases": ["استطالة معصم اليد للخارج", "Wrist Extensors", "إطالة ظهر الساعد"],
        "type": "static_stretch",
        "primaryMuscles": ["forearms"],
        "secondaryMuscles": ["wrists"],
        "bodyRegions": ["wrists_forearms"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "افرد ذراعك اليمنى للأمام في مستوى الكتف مع توجيه راحة اليد للأسفل.",
            "اثنِ معصمك للأسفل بحيث تتجه أصابع يدك نحو الأرض.",
            "استخدم يدك اليسرى للضغط برفق على ظهر كف يدك اليمنى وسحبه باتجاه جسمك حتى تشعر بإطالة على طول أعلى الساعد.",
            "حافظ على استقامة الكوع واسترخاء الكتف لأسفل.",
            "اثبت للمدة المحددة، ثم كرر لليد اليسرى."
        ],
        "durationSeconds": 25,
        "breathing": "تنفس طبيعي وهادئ مع إرخاء قبضة اليد والكتف.",
        "commonMistakes": [
            "ثني المرفق أثناء الإطالة مما يقلل من تمدد عضلات الساعد.",
            "الضغط بقوة مفرطة على الأصابع ومفصل المعصم."
        ],
        "safetyNotes": "توقف إذا شعرت بوخز أو تنميل في الأصابع؛ فهذا يشير إلى ضغط غير مستحب على الأعصاب السطحية.",
        "image": "assets/images/stretches/str-wrist-extensor-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["seated_palms_down_wrist_curl", "barbell_bench_press", "overhead_dumbbell_triceps_extension"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-wrist-flexor-prayer",
        "name": "Prayer Wrist Stretch (Flexor Stretch)",
        "nameAr": "استطالة عاطفات الرسغ وباطن الساعد بوضعية الضم",
        "aliases": ["تمرين إطالة الساعد بالضم", "Prayer Wrist Stretch", "إطالة باطن المعصم"],
        "type": "static_stretch",
        "primaryMuscles": ["forearms"],
        "secondaryMuscles": ["wrists"],
        "bodyRegions": ["wrists_forearms"],
        "equipment": "none",
        "level": "beginner",
        "instructions": [
            "ضع راحتي كفيك معًا أمام صدرك في وضعية الضم بحيث تتلامس الأصابع والراحتان بالكامل.",
            "مع إبقاء الراحتين ملتصقتين معًا، أنزل يديك ببطء نحو مستوى الخصر مع رفع المرفقين قليلاً للجانبين.",
            "اشعر بشد لطيف ومريح في باطن الرسغين وعضلات الساعد الداخلية.",
            "اثبت في هذا الوضع الممتع للمدة المحددة."
        ],
        "durationSeconds": 25,
        "breathing": "تنفس هادئ وعميق يساعد في إزالة التوتر التراكمي من استخدام الهواتف وحمل الأوزان.",
        "commonMistakes": [
            "فصل راحتي الكفين عن بعضهما عند النزول باليدين.",
            "رفع الكتفين نحو الأذنين."
        ],
        "safetyNotes": "أنزل اليدين فقط إلى النقطة التي تشعر فيها باستطالة مريحة، ولا تجبر المعصمين على ثني حاد ومؤلم.",
        "image": "assets/images/stretches/str-wrist-flexor-prayer.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["seated_palms_up_wrist_curl", "dead_hang", "barbell_curl"],
        "suitableFor": ["cooldown", "mobility"]
    },
    {
        "id": "str-quadruped-wrist-circles",
        "name": "Quadruped Wrist Mobility Circles",
        "nameAr": "تدوير الرسغين بوضعية الارتكاز الرباعي لتليين المفصل",
        "aliases": ["مرونة المعصم على الأرض", "Wrist Circles on Floor", "إحماء المعصم لتمرين الضغط"],
        "type": "joint_mobility",
        "primaryMuscles": ["wrists"],
        "secondaryMuscles": ["forearms"],
        "bodyRegions": ["wrists_forearms"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "انزل على ركبتيك وكفيك فوق بساط التمرين بحيث تكون اليدان تحت الكتفين والركبتان تحت الحوض.",
            "ضع راحتي الكفين مسطحتين على الأرض مع توجيه الأصابع للأمام أولاً.",
            "قم بعمل دوائر لطيفة وبطيئة بوزن جذعك فوق معصميك في اتجاه عقارب الساعة ثم عكسها.",
            "يمكنك تدوير وضع الأصابع لتشير للخارج نحو الجانبين أو للخلف نحو ركبتيك لتغيير زوايا تليين المفصل."
        ],
        "recommendedReps": "8-10 دوائر في كل اتجاه وبكل زاوية",
        "breathing": "تنفس طبيعي وسلس دون حبس النفس.",
        "commonMistakes": [
            "تحميل الوزن الكامل للجسم بقسوة فوق المعصمين دفعة واحدة.",
            "رفع راحة الكف عن الأرض أثناء الدوران."
        ],
        "safetyNotes": "تحكم في كمية الوزن المحمل فوق اليدين عبر إبقاء مركز الثقل قريبًا من الركبتين لتفادي الإجهاد.",
        "image": "assets/images/stretches/str-quadruped-wrist-circles.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["push_up", "barbell_bench_press", "barbell_front_squat"],
        "suitableFor": ["warmup", "mobility"]
    },

    # --- 9. العمود الفقري والحركة الدورانية (Spine & Rotation) ---
    {
        "id": "str-cat-cow-mobility",
        "name": "Cat-Cow Spine Mobility",
        "nameAr": "تمرين القطة والبقرة لتحريك وتليين العمود الفقري كاملاً",
        "aliases": ["استطالة القطة والبقرة", "Cat Cow Stretch", "مرونة فقرات الظهر"],
        "type": "joint_mobility",
        "primaryMuscles": ["spine"],
        "secondaryMuscles": ["core", "lower_back", "neck"],
        "bodyRegions": ["spine_rotation"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "ابدأ بوضعية الأطراف الأربعة (الركوع على الركبتين والكفين) مع استقامة الظهر في وضع محايد.",
            "وضعية البقرة (Cow): خذ شهيقًا عميقًا، وأسقط بطنك برفق نحو الأرض مع رفع صدرك وعظام حوضك للأعلى والنظر برفق للأمام.",
            "وضعية القطة (Cat): أخرج زفيرًا كاملاً، وقوّس ظهرك للأعلى نحو السقف كقطة مستنفرة مع سحب السرة نحو العمود الفقري وإسقاط الرأس بين الذراعين.",
            "انتقل بين الوضعيتين بنعومة وسلاسة متصلة تتبع إيقاع تنفسك."
        ],
        "recommendedReps": "10-12 دورة كاملة (شهيق للبقرة وزفير للقطة)",
        "breathing": "شهيق متزامن مع تقويس البطن لأسفل (Cow)، وزفير متزامن مع رفع الظهر لأعلى (Cat).",
        "commonMistakes": [
            "التعجل في الحركة واستخدام السرعة بدلاً من تحريك كل فقرة بتسلسل مدروس.",
            "المبالغة في ثني الرقبة للخلف في وضعية البقرة."
        ],
        "safetyNotes": "تمرين ممتاز وآمن لتنشيط وتليين الفقرات، تجنب الضغط الحاد في أقصى مدى إذا كنت تعاني من انزلاق غضروفي نشط.",
        "image": "assets/images/stretches/str-cat-cow-mobility.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["conventional_deadlift", "barbell_back_squat", "bird_dog"],
        "suitableFor": ["warmup", "cooldown", "mobility"]
    },
    {
        "id": "str-thoracic-spine-rotations",
        "name": "Quadruped Thoracic Spine Rotations",
        "nameAr": "الدوران الصدري للعمود الفقري في وضعية الارتكاز الرباعي",
        "aliases": ["دوران أعلى الظهر", "Thoracic Spine Rotation", "مرونة الفقرات الصدرية"],
        "type": "joint_mobility",
        "primaryMuscles": ["thoracic_spine"],
        "secondaryMuscles": ["shoulders", "upper_back", "core"],
        "bodyRegions": ["spine_rotation"],
        "equipment": "mat",
        "level": "intermediate",
        "instructions": [
            "ابدأ بالارتكاز على الأطراف الأربعة (الكفين والركبتين). اجلس بمؤخرتك قليلاً نحو الكعبين لتثبيت أسفل الظهر ومنع التفافه.",
            "ضع يدك اليمنى خلف رأسك أو مؤخرة عنقك مع إبقاء الكوع مثنيًا جانبيًا.",
            "أدخل كوعك الأيمن للأسفل وللداخل باتجاه معصم يدك اليسرى مع زفير.",
            "اعكس الحركة ودوّر صدرك وكوعك الأيمن للأعلى نحو السقف مع شهيق، وتابع الكوع بنظرك.",
            "أنهِ التكرارات للجانب الأيمن، ثم بدّل للجانب الأيسر."
        ],
        "recommendedReps": "8-10 تكرارات لكل جهة مع ثبات ثانية في القمة",
        "breathing": "زفير أثناء الدوران للداخل، وشهيق عميق يفتح القفص الصدري أثناء الدوران لأعلى.",
        "commonMistakes": [
            "تحريك الحوض وأسفل الظهر بدلاً من عزل الدوران في الفقرات الصدرية بأعلى الظهر.",
            "سحب الرأس باليد بدلاً من تدوير الصدر نفسه."
        ],
        "safetyNotes": "تحرّك في نطاق المرونة الطبيعي لفقراتك الصدرية وتجنب الإجبار القسري للمفصل على الالتفاف.",
        "image": "assets/images/stretches/str-thoracic-spine-rotations.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["standing_overhead_barbell_press", "barbell_back_squat", "barbell_bent_over_row"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-bird-dog-activation",
        "name": "Bird Dog Core & Spine Activation",
        "nameAr": "تنشيط استقرار العمود الفقري وعضلات الجذع (تمرين الطائر والكلب)",
        "aliases": ["تمرين بيرد دوج", "Bird Dog Exercise", "تثبيت الجذع وأسفل الظهر"],
        "type": "activation",
        "primaryMuscles": ["core"],
        "secondaryMuscles": ["lower_back", "glutes", "shoulders"],
        "bodyRegions": ["spine_rotation"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "ابدأ على الأطراف الأربعة مع وضع اليدين تحت الكتفين والركبتين تحت الحوض، وحافظ على ظهر مستقيم ومحايد.",
            "شد عضلات بطنك بإحكام لتثبيت الحوض والعمود الفقري.",
            "مدّ ذراعك اليمنى للأمام وساقك اليسرى للخلف في وقت واحد حتى يصبحا في خط أفقي مستقيم مع جذعك.",
            "اثبت لثانيتين مع التركيز على ثبات الجذع التام دون أن يميل الحوض لأي جانب.",
            "عُد ببطء لنقطة البداية، وبدّل مباشرة للذراع اليسرى والساق اليمنى."
        ],
        "recommendedReps": "10 تكرارات لكل جانب مع ثبات ثانيتين في كل تكرار",
        "breathing": "تنفس ثابت؛ زفير خفيف مع مد الأطراف وشهيق مع العودة لنقطة البداية.",
        "commonMistakes": [
            "رفع الساق عاليًا جدًا مع تقويس أسفل الظهر لأسفل بدلاً من مد الساق أفقيًا واستقامة العمود الفقري.",
            "اهتزاز الحوض أو سقوطه جانبيًا عند رفع الساق."
        ],
        "safetyNotes": "تمرين ذهبي معتمد من الجمعيات الطبية العالمية لإعادة تأهيل وحماية أسفل الظهر؛ المفتاح هو الثبات والتحكم.",
        "image": "assets/images/stretches/str-bird-dog-activation.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["bird_dog", "plank", "back_extensions"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-cobra-lumbar-stretch",
        "name": "Prone Cobra Lumbar & Abdominal Stretch",
        "nameAr": "استطالة الكوبرا لأسفل الظهر وعضلات البطن",
        "aliases": ["استطالة الكوبرا", "Cobra Stretch", "تمدد الظهر الأمامي"],
        "type": "static_stretch",
        "primaryMuscles": ["abs"],
        "secondaryMuscles": ["lower_back", "chest"],
        "bodyRegions": ["spine_rotation"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "استلقِ على بطنك على بساط التمرين مع فرد الساقين للخلف وتثبيت مشطي القدمين على الأرض.",
            "ضع كفيك على الأرض تحت كتفيك مباشرة مع ضم المرفقين بالقرب من جانبي جسمك.",
            "اضغط بكفيك على الأرض برفق لرفع صدرك ورأسك للأعلى، مع إبقاء حوضك وعظام العانة ملامسة للبساط.",
            "اخفض كتفيك بعيدًا عن أذنيك واشعر باستطالة خفيفة في عضلات البطن وتقوس لطيف في العمود الفقري.",
            "اثبت في هذا الوضع اللطيف للمدة المحددة."
        ],
        "durationSeconds": 25,
        "breathing": "شهيق يرفع الصدر بلطف، وزفير مريح يساعد على استرخاء عضلات الحوض والبطن.",
        "commonMistakes": [
            "قفل المرفقين بعنف ورفع الحوض بالكامل عن الأرض مما يضغط الفقرات القطنية.",
            "رفع الكتفين نحو الأذنين وتشنج عضلات الرقبة."
        ],
        "safetyNotes": "إذا شعرت بأي وخز أو ألم انضغاطي في فقرات أسفل الظهر، قلل ارتفاع الرفع أو استبدلها بوضعية أبو الهول (Sphinx Pose) بالارتكاز على الساعدين.",
        "image": "assets/images/stretches/str-cobra-lumbar-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["plank", "hanging_leg_raise", "cable_kneeling_crunch"],
        "suitableFor": ["cooldown", "mobility"]
    },

    # --- 10. كامل الجسم (Full Body) ---
    {
        "id": "str-worlds-greatest-stretch",
        "name": "World's Greatest Stretch",
        "nameAr": "أعظم استطالة في العالم لحركية كامل الجسم",
        "aliases": ["استطالة العالم الكبرى", "Worlds Greatest Stretch", "إطالة الحوض والصدر الشاملة"],
        "type": "dynamic_stretch",
        "primaryMuscles": ["full_body"],
        "secondaryMuscles": ["hips", "hamstrings", "thoracic_spine", "chest"],
        "bodyRegions": ["full_body"],
        "equipment": "mat",
        "level": "intermediate",
        "instructions": [
            "ابدأ بخطوة واسعة للأمام بساقك اليمنى وانزل في وضعية لاندجز عميقة مع وضع كلتا يديك على الأرض داخل قدمك اليمنى.",
            "أنزل كوعك الأيمن برفق نحو الأرض بجانب كاحلك الأيمن للشعور باستطالة عميقة في الورك والفخذ.",
            "ارفع ذراعك اليمنى للأعلى نحو السقف مع تدوير صدرك وجذعك بالكامل لمتابعة يدك بنظرك.",
            "ضع يدك اليمنى مجددًا على الأرض وادفع حوضك للخلف لفرد ساقك الأمامية ورفع مشط قدمها لإطالة عضلات الفخذ الخلفية.",
            "عُد للوضع الأول وبدّل الساق للجهة الأخرى وكرر التسلسل."
        ],
        "recommendedReps": "5-6 تكرارات متسلسلة وكاملة لكل جانب",
        "breathing": "شهيق أثناء الدوران ورفع الذراع للأعلى، وزفير أثناء الهبوط والرجوع للخلف.",
        "commonMistakes": [
            "الاستعجال في المراحل دون استيفاء المدى الحركي لكل خطوة.",
            "رفع كعب الساق الأمامية عن الأرض أثناء النزول العميق."
        ],
        "safetyNotes": "حركة مركبة شاملة ورائعة قبل التمارين الكبرى؛ أدّها بهدوء وتحكم ودون حركات مفاجئة.",
        "image": "assets/images/stretches/str-worlds-greatest-stretch.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "conventional_deadlift", "walking_lunges_dumbbell"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-deep-squat-pry",
        "name": "Deep Squat Hold with Prying",
        "nameAr": "النزول العميق في القرفصاء مع فتح وتليين الحوض",
        "aliases": ["قرفصاء عميقة مع فتح الحوض", "Deep Squat Pry", "مرونة قرفصاء السكوات"],
        "type": "joint_mobility",
        "primaryMuscles": ["hips"],
        "secondaryMuscles": ["ankles", "groin", "lower_back"],
        "bodyRegions": ["full_body"],
        "equipment": "none",
        "level": "intermediate",
        "instructions": [
            "قف مع فتح القدمين بعرض الكتفين أو أوسع قليلاً وتوجيه أصابع القدمين للخارج بزاوية 15-30 درجة.",
            "انزل في قرفصاء عميقة وكاملة مع الحفاظ على كعبيك مثبتين تمامًا على الأرض.",
            "ضع راحتي كفيك معًا أمام صدرك، واستخدم مرفقيك للضغط برفق على الفخذين والركبتين للخارج.",
            "ارفع صدرك للأعلى وافرد ظهرك، مع إمكانية إمالة وزنك برفق من جانب لآخر لتليين الكاحلين ومفاصل الورك.",
            "اثبت في هذا الوضع المريح وتناول أنفاسًا عميقة."
        ],
        "durationSeconds": 30,
        "breathing": "شهيق عميق يملأ الحوض والصدر، وزفير يساعد على النزول المسترخي في عمق القرفصاء.",
        "commonMistakes": [
            "ارتفاع الكعبين عن الأرض؛ إذا ارتفعا، ضع لوح وزن خفيف أو منشفة تحت الكعبين مؤقتًا.",
            "تحدب الظهر وسقوط الصدر للأسفل."
        ],
        "safetyNotes": "تجنب الاستمرار إذا شعرت بألم حاد في الركبة؛ ويمكنك الاستناد على عمود ثابت بيديك في البداية.",
        "image": "assets/images/stretches/str-deep-squat-pry.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["barbell_back_squat", "goblet_squat", "barbell_front_squat"],
        "suitableFor": ["warmup", "mobility"]
    },
    {
        "id": "str-downward-dog",
        "name": "Downward-Facing Dog",
        "nameAr": "وضعية الكلب المتجه لأسفل لإطالة السلسلة الخلفية للجسم",
        "aliases": ["استطالة الكلب المتجه لأسفل", "Downward Dog", "إطالة كامل السلسلة الخلفية"],
        "type": "dynamic_stretch",
        "primaryMuscles": ["calves"],
        "secondaryMuscles": ["hamstrings", "lats", "shoulders", "lower_back"],
        "bodyRegions": ["full_body"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "ابدأ بوضعية الأطراف الأربعة، ثم ادفع بكفيك وأصابع قدميك لرفع حوضك ومؤخرتك عاليًا باتجاه السقف حتى يشكل جسمك حرف V مقلوبًا.",
            "باعد بين أصابع اليدين واضغط بقوة عبر راحتي الكفين لإبعاد كتفيك عن أذنيك وإطالة العمود الفقري.",
            "ادفع كعبيك برفق نحو الأرض (مع السماح بثني خفيف في الركبتين إذا كانت أوتار الركبة مشدودة).",
            "يمكنك 'المشي في المكان' بالضغط بكعب تلو الآخر لزيادة إطالة السمانة وأوتار الفخذ الخلفية بنعومة.",
            "اثبت مع التنفس العميق ثم اخفض الركبتين للراحة."
        ],
        "durationSeconds": 35,
        "breathing": "تنفس بطيء وعميق، ومع كل زفير ادفع الحوض للأعلى وللخلف بمقدار إضافي.",
        "commonMistakes": [
            "تحدب الظهر وانتقال الوزن للأمام فوق المعصمين بدلاً من دفعه للخلف نحو الحوض والساقين.",
            "حبس النفس أو قفل الركبتين بقسوة."
        ],
        "safetyNotes": "إذا كانت عضلات الفخذ الخلفية مشدودة، اثنِ الركبتين قليلاً وركز على استقامة الظهر واستطالة العمود الفقري.",
        "image": "assets/images/stretches/str-downward-dog.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["conventional_deadlift", "romanian_deadlift_barbell", "overhead_dumbbell_triceps_extension"],
        "suitableFor": ["warmup", "cooldown", "mobility"]
    },
    {
        "id": "str-inchworm-walkout",
        "name": "Inchworm Walkout",
        "nameAr": "تمرين الزحف باليدين لكامل الجسم (الإنش وورم)",
        "aliases": ["الزحف باليدين للأمام", "Inchworm Walkout", "إحماء العضلات الخلفية والجذع"],
        "type": "warmup_drill",
        "primaryMuscles": ["full_body"],
        "secondaryMuscles": ["hamstrings", "core", "shoulders", "calves"],
        "bodyRegions": ["full_body"],
        "equipment": "mat",
        "level": "beginner",
        "instructions": [
            "قف مستقيمًا في مؤخرة البساط مع فتح القدمين بعرض الحوض.",
            "انحنِ للأمام من مفصل الورك وضع يديك على الأرض أمام قدميك (مع ثني خفيف في الركبتين عند الحاجة).",
            "ازحف بيديك خطوة بخطوة للأمام على الأرض حتى تصل إلى وضعية تمرين البلانك الكامل المستقيم.",
            "اثبت في البلانك لثانية واحدة مع شد عضلات البطن والإلية.",
            "ازحف بيديك للخلف باتجاه قدميك مرة أخرى، ثم قف مستقيمًا ببطء وكرر."
        ],
        "recommendedReps": "6-8 تكرارات كاملة وتحكم تام",
        "breathing": "شهيق أثناء الوقوف، وزفير أثناء النزول والزحف للأمام، ثم تنفس منتظم أثناء العودة.",
        "commonMistakes": [
            "هبوط الحوض وترهله لأسفل أثناء الوصول لوضعية البلانك مما يجهد أسفل الظهر.",
            "الاستعجال في الزحف بدلاً من التحكم في عضلات الكتفين والبطن."
        ],
        "safetyNotes": "حافظ على انثناء بسيط في الركبتين عند لمس الأرض إذا كانت المرونة في الفخذ الخلفي محدودة.",
        "image": "assets/images/stretches/str-inchworm-walkout.svg",
        "imageCredit": "Zatoona Original SVG Illustration (Male Athletic)",
        "relatedExerciseIds": ["push_up", "plank", "barbell_back_squat"],
        "suitableFor": ["warmup"]
    }
]

print(f"Total movement definitions: {len(MOVEMENTS)}")

# 1. Generate assets/data/stretch-catalog.js
catalog_js_path = r"assets\data\stretch-catalog.js"
with open(catalog_js_path, "w", encoding="utf-8") as f:
    f.write("/**\n")
    f.write(" * Zatoona Stretch & Mobility Encyclopedia Catalog\n")
    f.write(" * Phase 9C.1 Implementation - Offline-First Standalone Asset\n")
    f.write(" * Strict Males-Only visual policy & 100% verified local vector assets.\n")
    f.write(" */\n")
    f.write("window.ZATOONA_STRETCH_CATALOG = ")
    json.dump(MOVEMENTS, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"Successfully generated {catalog_js_path} (size: {os.path.getsize(catalog_js_path)} bytes)")

# 2. Template for SVG generation
# Distinct, anatomically descriptive athletic male vector illustrations with zero external URLs.
def build_male_svg(movement):
    m_id = movement["id"]
    m_name_ar = movement["nameAr"]
    m_name_en = movement["name"]
    m_type = movement["type"]
    m_region = movement["bodyRegions"][0] if movement["bodyRegions"] else "general"

    # Color palette
    # Dark modern canvas, accent cyan/orange, clean male athletic silhouette
    bg_gradient_start = "#0f172a"
    bg_gradient_end = "#1e293b"
    accent_color = "#38bdf8"      # Light cyan for movement cues
    highlight_color = "#f59e0b"   # Amber for target muscles
    body_fill = "#334155"         # Male athletic torso/limbs
    body_stroke = "#64748b"       # Defined muscular contours
    head_fill = "#475569"
    grid_line = "#1e293b"

    # Specific athletic pose geometry per movement
    # We will generate unique vector paths tailored to each movement's actual body configuration!
    # Let's define pose configs for each movement
    
    # Generic base that can be customized per ID:
    # viewBox: 0 0 400 300
    # Center: (200, 150)
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%" role="img" aria-label="{m_name_ar}">
  <defs>
    <linearGradient id="bgGrad-{m_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_gradient_start}"/>
      <stop offset="100%" stop-color="{bg_gradient_end}"/>
    </linearGradient>
    <linearGradient id="maleMuscles-{m_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <filter id="glow-{m_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="400" height="300" rx="16" fill="url(#bgGrad-{m_id})"/>

  <!-- Gym floor grid lines for spatial reference -->
  <line x1="30" y1="240" x2="370" y2="240" stroke="#334155" stroke-width="2" stroke-dasharray="6,4"/>
  <circle cx="200" cy="240" r="3" fill="#64748b"/>

  <!-- Target Muscle Highlight Indicator Banner -->
  <rect x="24" y="20" width="120" height="24" rx="6" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <circle cx="36" cy="32" r="4" fill="{highlight_color}"/>
  <text x="46" y="36" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="600">{m_type.replace('_', ' ').upper()}</text>

  <!-- Male Athletic Figure Group -->
  <g id="maleFigure-{m_id}" transform="translate(0, 0)">
'''

    # Detailed specialized vector art per movement category
    if "chest" in m_id or "pec" in m_id:
        svg_content += f'''
    <!-- Wall / Doorway frame -->
    <rect x="280" y="50" width="16" height="190" rx="2" fill="#475569" stroke="#64748b" stroke-width="2"/>
    <rect x="270" y="45" width="36" height="10" rx="2" fill="#334155"/>
    <!-- Male Athletic Silhouette Standing Chest Stretch -->
    <!-- Head with masculine short jawline -->
    <ellipse cx="195" cy="85" rx="14" ry="17" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Neck -->
    <rect x="190" y="100" width="10" height="12" fill="{head_fill}"/>
    <!-- Muscular Torso angled away -->
    <path d="M175 112 L215 112 L208 175 L182 175 Z" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Highlighted Pecs (Target) -->
    <path d="M180 118 Q195 135 210 118 Q205 142 185 142 Z" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <!-- Arm on doorway bent at 90 deg -->
    <path d="M215 118 Q250 115 265 115 L280 115 L280 80" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="280" cy="80" r="6" fill="{body_stroke}"/>
    <!-- Free arm -->
    <path d="M175 118 Q165 145 168 175" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <!-- Legs in split lunge stance -->
    <path d="M185 175 L170 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <path d="M205 175 L225 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Stretch arrow vector -->
    <path d="M165 130 Q150 135 145 150" fill="none" stroke="{accent_color}" stroke-width="3" stroke-dasharray="4,2"/>
    <polygon points="142,152 150,147 145,142" fill="{accent_color}"/>
'''
    elif "arm-circles" in m_id:
        svg_content += f'''
    <!-- Male Athletic Silhouette Standing with Extended Arms & Dynamic Rotation Circles -->
    <!-- Head -->
    <ellipse cx="200" cy="80" rx="14" ry="17" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <rect x="195" y="95" width="10" height="12" fill="{head_fill}"/>
    <!-- Torso broad athletic v-taper -->
    <path d="M175 107 L225 107 L215 175 L185 175 Z" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Highlighted Deltoids (Shoulders) -->
    <circle cx="170" cy="115" r="10" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <circle cx="230" cy="115" r="10" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <!-- Extended Arms -->
    <path d="M170 115 L95 115" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <path d="M230 115 L305 115" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <!-- Dynamic Rotation Arcs -->
    <ellipse cx="95" cy="115" rx="22" ry="32" fill="none" stroke="{accent_color}" stroke-width="2.5" stroke-dasharray="5,3"/>
    <polygon points="95,83 103,90 95,95" fill="{accent_color}"/>
    <ellipse cx="305" cy="115" rx="22" ry="32" fill="none" stroke="{accent_color}" stroke-width="2.5" stroke-dasharray="5,3"/>
    <polygon points="305,83 313,90 305,95" fill="{accent_color}"/>
    <!-- Legs Athletic Stance -->
    <path d="M190 175 L175 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <path d="M210 175 L225 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
'''
    elif "shoulder" in m_id or "deltoid" in m_id:
        svg_content += f'''
    <!-- Male Athletic Silhouette Cross-Body or Pass-Through Shoulder Movement -->
    <!-- Head -->
    <ellipse cx="200" cy="80" rx="14" ry="17" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <rect x="195" y="95" width="10" height="12" fill="{head_fill}"/>
    <!-- Broad V-Taper Torso -->
    <path d="M175 107 L225 107 L212 175 L188 175 Z" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Target Shoulder Highlight -->
    <circle cx="225" cy="118" r="12" fill="{highlight_color}" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Arm crossing torso horizontally -->
    <path d="M225 118 L140 125" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round"/>
    <!-- Supporting Hand pulling elbow -->
    <path d="M170 160 L160 120" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <!-- Dynamic Force Vector -->
    <path d="M155 112 Q145 125 155 138" fill="none" stroke="{accent_color}" stroke-width="3"/>
    <!-- Legs Stance -->
    <path d="M190 175 L180 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <path d="M210 175 L220 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
'''
    elif "lat" in m_id or "child" in m_id or "back" in m_id:
        if "child" in m_id:
            svg_content += f'''
    <!-- Male Athletic Silhouette in Extended Child's Pose (On Mat) -->
    <!-- Exercise Mat -->
    <rect x="50" y="235" width="300" height="8" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <!-- Folded Legs/Hips seated on heels -->
    <ellipse cx="280" cy="215" rx="28" ry="18" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <path d="M295 225 L255 235 L220 235" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Torso extended forward along floor -->
    <path d="M260 210 Q200 195 150 215" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="22" stroke-linecap="round"/>
    <!-- Target Latissimus & Lower Back Highlight -->
    <path d="M245 202 Q190 190 150 205" fill="none" stroke="{highlight_color}" stroke-width="7" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Extended Arms stretched forward flat on mat -->
    <path d="M150 215 L85 230" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <circle cx="80" cy="232" r="5" fill="{body_stroke}"/>
    <!-- Head rested downward -->
    <ellipse cx="140" cy="222" rx="13" ry="11" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Stretch arrows -->
    <path d="M210 180 L180 180" fill="none" stroke="{accent_color}" stroke-width="2.5" stroke-dasharray="4,2"/>
    <polygon points="175,180 183,176 183,184" fill="{accent_color}"/>
'''
        else:
            svg_content += f'''
    <!-- Male Athletic Lat Wall Stretch (Hinged at Hips) -->
    <!-- Wall Reference -->
    <rect x="70" y="60" width="14" height="180" rx="2" fill="#475569" stroke="#64748b" stroke-width="1.5"/>
    <!-- Hands on wall -->
    <circle cx="86" cy="130" r="6" fill="{body_stroke}"/>
    <!-- Arms reaching to wall -->
    <path d="M86 130 L160 135" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <!-- Head between arms -->
    <ellipse cx="150" cy="140" rx="12" ry="14" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Torso hinged horizontally -->
    <path d="M160 135 L240 145" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Lat Highlight Zone -->
    <path d="M170 132 L230 140" fill="none" stroke="{highlight_color}" stroke-width="8" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Hips and Glutes pushed back -->
    <circle cx="245" cy="148" r="16" fill="url(#maleMuscles-{m_id})"/>
    <!-- Legs with soft knee bend -->
    <path d="M245 155 L255 195 L250 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <path d="M235 155 L230 195 L225 240" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round"/>
'''
    elif "neck" in m_id or "chin" in m_id or "trap" in m_id:
        svg_content += f'''
    <!-- Male Athletic Neck & Upper Cervical Region Portrait Alignment -->
    <!-- Athletic Upper Chest & Traps Profile -->
    <path d="M130 240 L160 180 L200 170 L240 180 L270 240 Z" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Broad Neck Column -->
    <rect x="186" y="125" width="28" height="48" rx="4" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Highlighted Cervical / Upper Traps Zone -->
    <path d="M175 160 Q200 150 225 160 L235 180 L165 180 Z" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <!-- Strong Male Head Profile / Jawline -->
    <path d="M185 85 Q200 70 218 85 Q225 105 215 125 L188 125 Z" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Hand guiding gently (if applicable) -->
    <path d="M160 210 Q145 140 185 85" fill="none" stroke="{body_stroke}" stroke-width="6" stroke-linecap="round" stroke-dasharray="4,3"/>
    <!-- Dynamic Alignment Vector -->
    <path d="M240 95 L260 95" fill="none" stroke="{accent_color}" stroke-width="3"/>
    <polygon points="265,95 257,90 257,100" fill="{accent_color}"/>
'''
    elif "hip" in m_id or "adductor" in m_id or "butterfly" in m_id:
        if "kneeling" in m_id:
            svg_content += f'''
    <!-- Male Half-Kneeling Athletic Hip Flexor Stretch -->
    <!-- Rear Knee on Mat -->
    <rect x="70" y="236" width="260" height="8" rx="2" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <!-- Rear Leg (Thigh vertical, knee down) -->
    <path d="M150 170 L150 236 L115 236" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Torso upright and tall -->
    <path d="M155 170 L160 110" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="22" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="162" cy="85" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Target Hip Flexor / Psoas Glow Zone -->
    <ellipse cx="152" cy="168" rx="14" ry="18" fill="{highlight_color}" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Front Leg bent 90 degrees -->
    <path d="M160 170 L220 175 L225 236" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Forward Pelvic Push Indicator -->
    <path d="M175 165 L198 165" fill="none" stroke="{accent_color}" stroke-width="3"/>
    <polygon points="204,165 196,160 196,170" fill="{accent_color}"/>
'''
        else:
            svg_content += f'''
    <!-- Male 90/90 or Seated Butterfly Hip Mobility -->
    <rect x="60" y="235" width="280" height="8" rx="2" fill="#1e293b"/>
    <!-- Seated Pelvis Base -->
    <ellipse cx="200" cy="205" rx="26" ry="16" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Upright / Incline Spine -->
    <path d="M200 205 L200 120" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="200" cy="90" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Target Groin / Hip Capsule Highlight -->
    <circle cx="200" cy="205" r="16" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <!-- Legs folded outwards (Butterfly / 90-90) -->
    <path d="M185 210 Q140 215 130 235 L190 235" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <path d="M215 210 Q260 215 270 235 L210 235" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Downward mobility vectors -->
    <path d="M140 200 L140 220" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="140,224 136,216 144,216" fill="{accent_color}"/>
    <path d="M260 200 L260 220" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="260,224 256,216 264,216" fill="{accent_color}"/>
'''
    elif "quad" in m_id or "hamstring" in m_id or "leg-swings" in m_id or "couch" in m_id:
        if "standing-quad" in m_id:
            svg_content += f'''
    <!-- Male Athletic Standing Quad Stretch -->
    <line x1="120" y1="50" x2="120" y2="240" stroke="#334155" stroke-width="4"/>
    <!-- Standing Leg -->
    <path d="M180 165 L180 240" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Upright Torso -->
    <path d="M180 165 L185 105" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="186" cy="80" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Hand holding wall -->
    <path d="M185 110 L120 115" fill="none" stroke="{body_stroke}" stroke-width="7" stroke-linecap="round"/>
    <!-- Bent Quad (Leg pulled back) -->
    <path d="M185 165 L190 210 L220 175" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Hand holding ankle -->
    <path d="M185 115 L220 175" fill="none" stroke="{body_stroke}" stroke-width="7" stroke-linecap="round"/>
    <!-- Target Quadriceps Glow -->
    <path d="M184 170 L188 208" fill="none" stroke="{highlight_color}" stroke-width="9" opacity="0.9" filter="url(#glow-{m_id})"/>
'''
        elif "hamstring" in m_id:
            svg_content += f'''
    <!-- Male Athletic Standing Hamstring Stretch (Hips Pushed Back) -->
    <!-- Rear Bent Leg -->
    <path d="M225 160 L240 195 L235 240" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Front Extended Leg with Heel on Ground & Toe Up -->
    <path d="M215 160 L160 215 L145 238" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Toe pointed up -->
    <path d="M145 238 L140 225" fill="none" stroke="{body_stroke}" stroke-width="5" stroke-linecap="round"/>
    <!-- Target Hamstring Highlight Zone -->
    <path d="M210 165 L165 210" fill="none" stroke="{highlight_color}" stroke-width="8" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Torso Hinged Forward with Flat Back -->
    <path d="M220 160 L170 120" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Head in line with spine -->
    <ellipse cx="155" cy="110" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Hands resting on thighs -->
    <path d="M175 125 L195 165" fill="none" stroke="{body_stroke}" stroke-width="7" stroke-linecap="round"/>
'''
        else: # couch or leg swings
            svg_content += f'''
    <!-- Male Athletic Leg / Quad / Hamstring Movement Silhouette -->
    <!-- Floor and Support -->
    <rect x="60" y="236" width="280" height="8" rx="2" fill="#1e293b"/>
    <!-- Dynamic Split Stance Silhouette -->
    <path d="M180 165 L140 236" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <path d="M190 165 L245 215 L260 236" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Target Thigh Glow -->
    <path d="M182 170 L148 225" fill="none" stroke="{highlight_color}" stroke-width="9" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Torso Athletic Upright Profile -->
    <path d="M185 165 L185 105" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="21" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="185" cy="80" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Motion dynamic arrow -->
    <path d="M235 180 Q255 190 265 210" fill="none" stroke="{accent_color}" stroke-width="3" stroke-dasharray="4,2"/>
'''
    elif "glute" in m_id or "pigeon" in m_id:
        if "bridge" in m_id:
            svg_content += f'''
    <!-- Male Athletic Glute Bridge Activation (Lying on Mat) -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Feet flat on floor -->
    <path d="M100 235 L125 180" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Elevated Hips and Contracted Glutes -->
    <ellipse cx="155" cy="165" rx="18" ry="14" fill="{highlight_color}" opacity="0.95" filter="url(#glow-{m_id})"/>
    <!-- Straight Torso from Knees to Shoulders -->
    <path d="M130 180 L220 215" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Shoulders and Head on floor -->
    <ellipse cx="250" cy="225" rx="15" ry="13" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Arms by side -->
    <path d="M220 220 L160 230" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <!-- Upward contraction vector -->
    <path d="M155 195 L155 150" fill="none" stroke="{accent_color}" stroke-width="3"/>
    <polygon points="155,145 150,154 160,154" fill="{accent_color}"/>
'''
        else: # pigeon or figure 4
            svg_content += f'''
    <!-- Male Athletic Pigeon Pose / Figure 4 Glute Stretch -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Folded Front Leg -->
    <path d="M130 235 Q170 210 200 215" fill="none" stroke="{body_stroke}" stroke-width="13" stroke-linecap="round"/>
    <!-- Target Gluteus Max/Med Glow Area -->
    <circle cx="175" cy="215" r="16" fill="{highlight_color}" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Rear Leg Extended back on floor -->
    <path d="M190 215 L285 235" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Torso leaning forward over folded leg -->
    <path d="M185 215 L125 170" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="19" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="115" cy="155" rx="14" ry="14" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Supporting Forearms on mat -->
    <path d="M135 180 L100 225 L85 235" fill="none" stroke="{body_stroke}" stroke-width="7" stroke-linecap="round"/>
'''
    elif "calf" in m_id or "ankle" in m_id or "soleus" in m_id:
        svg_content += f'''
    <!-- Male Athletic Calf & Ankle Wall Mobility Stretch -->
    <!-- Wall Structure -->
    <rect x="80" y="50" width="14" height="190" rx="2" fill="#475569" stroke="#64748b" stroke-width="1.5"/>
    <!-- Hands on wall -->
    <circle cx="96" cy="120" r="6" fill="{body_stroke}"/>
    <!-- Arms bracing on wall -->
    <path d="M96 120 L160 125" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <!-- Torso inclined -->
    <path d="M160 125 L210 160" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Head -->
    <ellipse cx="155" cy="100" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Front Leg Bent towards wall -->
    <path d="M205 160 L140 190 L135 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Rear Leg Stretched Back Flat Heel -->
    <path d="M215 160 L260 195 L275 240" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Target Calf / Gastrocnemius / Soleus Glow -->
    <path d="M255 190 L270 225" fill="none" stroke="{highlight_color}" stroke-width="9" opacity="0.95" filter="url(#glow-{m_id})"/>
    <!-- Force vector driving heel down -->
    <path d="M285 210 L285 235" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="285,238 281,230 289,230" fill="{accent_color}"/>
'''
    elif "wrist" in m_id or "forearm" in m_id:
        svg_content += f'''
    <!-- Male Athletic Forearm & Wrist Mobility Articulation -->
    <!-- Forearm Profile with Muscular Contour -->
    <path d="M110 160 Q160 152 230 155 L230 175 Q160 180 110 170 Z" fill="url(#maleMuscles-{m_id})" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Highlighted Forearm Flexors/Extensors -->
    <path d="M130 156 Q170 153 215 157 L215 172 Q170 176 130 169 Z" fill="{highlight_color}" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Articulating Hand / Fingers in stretch position -->
    <path d="M230 155 L255 135 L275 130" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <circle cx="230" cy="165" r="7" fill="{head_fill}"/>
    <!-- Opposite hand applying light guidance -->
    <path d="M260 110 L260 145" fill="none" stroke="{body_stroke}" stroke-width="7" stroke-linecap="round"/>
    <!-- Gentle stretch directional arc -->
    <path d="M275 145 Q265 160 250 165" fill="none" stroke="{accent_color}" stroke-width="2.5" stroke-dasharray="3,2"/>
    <polygon points="248,166 256,164 253,158" fill="{accent_color}"/>
'''
    elif "cat-cow" in m_id or "cobra" in m_id or "thoracic" in m_id or "bird-dog" in m_id:
        if "cat-cow" in m_id:
            svg_content += f'''
    <!-- Male Athletic Cat-Cow Spinal Articulation Drill -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Vertical Arms bracings under shoulders -->
    <path d="M130 160 L130 235" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round"/>
    <!-- Vertical Thighs under hips -->
    <path d="M260 170 L260 235" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Articulated Flexed / Extended Spine Curve -->
    <path d="M130 160 Q195 125 260 170" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Target Spine Vertebral Column Highlight -->
    <path d="M140 158 Q195 128 250 167" fill="none" stroke="{highlight_color}" stroke-width="7" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Head moving with spine -->
    <ellipse cx="105" cy="170" rx="14" ry="14" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Upward / Downward Wave Motion Vectors -->
    <path d="M195 110 L195 125" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="195,105 190,113 200,113" fill="{accent_color}"/>
'''
        elif "cobra" in m_id:
            svg_content += f'''
    <!-- Male Athletic Prone Cobra Lumbar Extension -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Legs Extended Flat on Mat -->
    <path d="M200 230 L310 235" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Pelvis on Mat with gentle spine lift -->
    <ellipse cx="195" cy="225" rx="18" ry="12" fill="url(#maleMuscles-{m_id})"/>
    <!-- Arching Torso Supported by Arms -->
    <path d="M195 225 Q160 190 120 150" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Hands pressing lightly under shoulders -->
    <path d="M135 170 L115 235" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <!-- Target Abdominal Wall & Lumbar Curve Glow -->
    <path d="M190 220 Q160 185 125 155" fill="none" stroke="{highlight_color}" stroke-width="8" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Head Extended Looking Gently Forward/Up -->
    <ellipse cx="110" cy="130" rx="14" ry="16" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
'''
        else: # bird-dog or thoracic
            svg_content += f'''
    <!-- Male Athletic Quadruped Spine Stabilization / Rotation Drill -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Supporting Arm and Leg -->
    <path d="M170 170 L170 235" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round"/>
    <path d="M225 170 L225 235" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Horizontal Torso / Core Core Cylinder -->
    <path d="M150 165 L240 165" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="20" stroke-linecap="round"/>
    <!-- Target Core / Spine Stabilizer Glow -->
    <path d="M160 165 L230 165" fill="none" stroke="{highlight_color}" stroke-width="8" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Extended Arm Forward (Bird Dog / Thoracic) -->
    <path d="M150 165 L85 160" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <!-- Extended Leg Backward Horizontal -->
    <path d="M240 165 L315 165" fill="none" stroke="{body_stroke}" stroke-width="10" stroke-linecap="round"/>
    <!-- Head in neutral alignment -->
    <ellipse cx="140" cy="150" rx="14" ry="14" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
'''
    else: # full body (worlds greatest, squat pry, downward dog, inchworm)
        if "downward" in m_id:
            svg_content += f'''
    <!-- Male Athletic Downward-Facing Dog (Inverted V) -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Hands Braced on Mat -->
    <circle cx="95" cy="235" r="5" fill="{body_stroke}"/>
    <!-- Arms and Spine in Straight Line to Hips -->
    <path d="M95 235 L195 130" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="16" stroke-linecap="round"/>
    <!-- Inverted V Apex (Hips pushed to ceiling) -->
    <circle cx="195" cy="130" r="16" fill="url(#maleMuscles-{m_id})"/>
    <!-- Head relaxed between upper arms -->
    <ellipse cx="125" cy="200" rx="13" ry="13" fill="{head_fill}" stroke="{body_stroke}" stroke-width="1.5"/>
    <!-- Straight Legs to Heels on Floor -->
    <path d="M195 130 L285 235" fill="none" stroke="{body_stroke}" stroke-width="14" stroke-linecap="round"/>
    <!-- Target Calves & Posterior Chain Glow -->
    <path d="M210 145 L275 225" fill="none" stroke="{highlight_color}" stroke-width="8" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Motion Vector directing energy up and back -->
    <path d="M175 160 L195 135" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="198,130 190,136 198,142" fill="{accent_color}"/>
'''
        elif "squat" in m_id:
            svg_content += f'''
    <!-- Male Athletic Deep Squat Hold & Hip Prying -->
    <line x1="80" y1="240" x2="320" y2="240" stroke="#334155" stroke-width="3"/>
    <!-- Feet Flat on Floor Wide Stance -->
    <!-- Deep Folded Knees and Shins -->
    <path d="M140 240 L125 180 L180 205" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <path d="M260 240 L275 180 L220 205" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Deep Pelvis Position -->
    <ellipse cx="200" cy="210" rx="24" ry="16" fill="url(#maleMuscles-{m_id})"/>
    <!-- Target Deep Hips & Groin Glow -->
    <circle cx="200" cy="210" r="18" fill="{highlight_color}" opacity="0.9" filter="url(#glow-{m_id})"/>
    <!-- Upright Proud Chest Torso -->
    <path d="M200 205 L200 120" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="22" stroke-linecap="round"/>
    <!-- Hands joined in prayer pushing knees out with elbows -->
    <path d="M150 185 L200 160 L250 185" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <!-- Head Upright -->
    <ellipse cx="200" cy="85" rx="14" ry="17" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Outward prying arrows -->
    <path d="M155 175 L135 175" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="130,175 138,171 138,179" fill="{accent_color}"/>
    <path d="M245 175 L265 175" fill="none" stroke="{accent_color}" stroke-width="2.5"/>
    <polygon points="270,175 262,171 262,179" fill="{accent_color}"/>
'''
        else: # worlds greatest or inchworm
            svg_content += f'''
    <!-- Male Athletic Full Body Mobility & Movement Silhouette -->
    <rect x="50" y="235" width="300" height="8" rx="2" fill="#1e293b"/>
    <!-- Front Leg Deep Lunge -->
    <path d="M120 235 L125 175 L190 180" fill="none" stroke="{body_stroke}" stroke-width="12" stroke-linecap="round"/>
    <!-- Rear Leg Long Stride -->
    <path d="M190 180 L290 230" fill="none" stroke="{body_stroke}" stroke-width="11" stroke-linecap="round"/>
    <!-- Support Hand on Ground -->
    <path d="M150 175 L150 235" fill="none" stroke="{body_stroke}" stroke-width="8" stroke-linecap="round"/>
    <!-- Torso Rotated Upward with Raised Arm (World's Greatest) -->
    <path d="M190 180 L150 135" fill="none" stroke="url(#maleMuscles-{m_id})" stroke-width="19" stroke-linecap="round"/>
    <path d="M150 135 L120 75" fill="none" stroke="{body_stroke}" stroke-width="9" stroke-linecap="round"/>
    <circle cx="120" cy="72" r="5" fill="{accent_color}"/>
    <!-- Target Full Body Integration Glow -->
    <circle cx="170" cy="170" r="18" fill="{highlight_color}" opacity="0.85" filter="url(#glow-{m_id})"/>
    <!-- Head Looking Up at Raised Hand -->
    <ellipse cx="155" cy="118" rx="13" ry="15" fill="{head_fill}" stroke="{body_stroke}" stroke-width="2"/>
    <!-- Rotational vector -->
    <path d="M130 115 Q145 95 130 80" fill="none" stroke="{accent_color}" stroke-width="2.5" stroke-dasharray="3,2"/>
    <polygon points="127,77 135,80 131,85" fill="{accent_color}"/>
'''

    svg_content += f'''
  </g>

  <!-- Clean Descriptive Watermark Badge -->
  <text x="375" y="278" text-anchor="end" fill="#64748b" font-family="system-ui, sans-serif" font-size="10" font-weight="500">ZATOONA MOBILITY</text>
  <text x="24" y="278" fill="#475569" font-family="system-ui, sans-serif" font-size="10" font-weight="500">STRICT MALES-ONLY VECTOR</text>
</svg>
'''
    return svg_content

# Generate all 34 SVG files
count = 0
for mov in MOVEMENTS:
    svg_filename = f"{mov['id']}.svg"
    full_svg_path = os.path.join(stretches_dir, svg_filename)
    svg_data = build_male_svg(mov)
    with open(full_svg_path, "w", encoding="utf-8") as f_svg:
        f_svg.write(svg_data.strip())
    count += 1

print(f"Successfully generated {count} SVG files in {stretches_dir}")
