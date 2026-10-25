# تقرير التدقيق اللاحق لتغطية صور التمارين الرياضية (Phase 12.1C)
## Post-Implementation Coverage Reconciliation — Strict Read-Only Audit

- **المشروع:** Zatoona (تطبيق ويب تقدمي شخصي Offline-First PWA)
- **المسار المحلي:** `C:\Users\Lenovo\Documents\GitHub\zatoona`
- **تاريخ وساعة التدقيق:** 2026-10-25T17:22:00+03:00
- **نوع المهمة:** تدقيق فني صارم للقراءة فقط (Strict Read-Only Audit — No New Images or Production Mutations)
- **الحالة السابقة:** Phase 12.1B منفذة بنجاح واجتياز 10 أجنحة من أصل 10 (540 / 540 فحصًا بنسبة 100%)

---

## 1. حماية الحالة الحالية وسلامة ملفات الإنتاج

تم التحقق من سلامة البيئة وبصمات التشفير قبل الشروع في فحص الكتالوج:

1. **حالة مستودع Git (`git status --short`):**
   - ملفات الإنتاج (`index.html`, `zatoona.html`, `sw.js`, `manifest.json`, `assets/data/exercise-catalog.js`) نظيفة تمامًا وتطابق الالتزام الأخير لـ Phase 12.1B.
   - لا توجد أي تعديلات غير متعمدة أو مسارات مكسورة (`git diff --check` انتهى بكود 0 بدون أي أخطاء مسافات أو أسطر).
   - التعديلات السابقة لاختباري Phase 12.6.1 (`test_phase5b1_2_legacy_images.py` و `test_phase9c3_cooldown.py`) محفوظة كما هي.
2. **التطابق الثنائي لملفي HTML (`fc.exe /b`):**
   - الأمر: `fc.exe /b index.html zatoona.html`
   - النتيجة: **`FC: no differences encountered` (تطابق ثنائي بايت لبايت 100%)**.
3. **بصمات SHA-256 الحالية للملفات الأساسية:**
   - `index.html`: `10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957` (1,221,201 بايت)
   - `zatoona.html`: `10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957` (1,221,201 بايت)
   - `sw.js`: `7AB40099A5529823119CD5FB1A85AF88FAB26546FE2B8885D974B792063130C3` (20,545 بايت)
   - `assets/data/exercise-catalog.js`: `BC6320D1CA83A748F3F15722010388CDA2333FC7AEE3C267840AB6C42EDAAC26` (139,227 بايت)
   - `manifest.json`: `C872752E51F5B339BD3965370B5DF54B47CBAAAD398785F85D6453FD93C743E5` (1,022 بايت)

---

## 2. إعادة بناء جرد الكتالوج والعدد الفعلي للأصول

1. **العدد الفعلي لتمارين الكتالوج الشامل (`exercise-catalog.js`):**
   - تم التحقق من الكائن `window.ZATOONA_EXERCISE_CATALOG`.
   - العدد الفعلي المؤكد: **119 تمرينًا** بدقة.
   - يتوزع الكتالوج بين **63 تمرين مركب (Compound)** و **56 تمرين عزل (Isolation)**.
2. **إجمالي رسومات SVG المحلية على القرص (`assets/images/exercises/`):**
   - العدد الإجمالي المثبت: **31 ملف SVG** محلي.
   - يتألف من:
     * **12 رسم SVG كلاسيكي (Pre-12.1B):** `ex-a01-goblet-squat.svg` إلى `ex-b06-lunges.svg` (11 منها مرتبطة بتمارين في الكتالوج، ورسم للكرانش الأرضي).
     * **19 رسم SVG جديد منفذ في Phase 12.1B:** `ex-barbell-back-squat.svg` إلى `ex-seated-palms-up-wrist-curl.svg`.
3. **أصول الرسوم الأخرى في المشروع (للتأكيد وعدم الخلط):**
   - الاستطالات (`assets/images/stretches/`): 34 ملف SVG.
   - الإحماء (`assets/images/warmup/`): 6 ملفات SVG.
   - التهدئة (`assets/images/cooldown/`): 6 ملفات SVG.
   - لم يتم استخدام أي من هذه الملفات كصور تمارين مقاومة، بما يتفق تمامًا مع التعليمات الصارمة.

---

## 3. تدقيق جودة الرسومات الجديدة والتكامل البصري

تم فحص جميع ملفات الـ SVG الـ 31 الموجودة على القرص فحصًا برمجيًا وهيكليًا صارمًا:

1. **سلامة بنية XML ونسب العرض:**
   - جميع الملفات الـ 31 (بما فيها الـ 19 الجديدة) تشكل مستندات XML صالحة ومغلقة بإحكام وتُقرأ بنجاح عبر `xml.etree.ElementTree`.
   - جميع الملفات تمتلك سمة `viewBox="0 0 300 200"` و `width="100%"` و `height="100%"` متناسقة تمامًا مع إطار العرض في التطبيق.
2. **الخلو التام من الصور النقطية والسكربتات والروابط الخارجية:**
   - صفر (0) صور مضمنة بصيغة Base64 (`data:image`).
   - صفر (0) وسوم سكربت `<script>`.
   - صفر (0) مراجع شبكية أو خطوط خارجية (`http://` أو `https://`) باستثناء فضاء الأسماء القياسي لاتحاد الويب `http://www.w3.org/2000/svg`.
3. **سياسة إظهار الرجال البالغين فقط (Adult Males Only):**
   - تم التحقق من مطابقة جميع الشخصيات البشرية المصورة لسياسة التطبيق (رجال بالغون فقط).
4. **أحجام الملفات:**
   - تتراوح أحجام الرسومات الـ 19 الجديدة بين **2,335 بايت و 3,333 بايت** (متوسط 2.8 كيلوبايت)، مما يضمن تحميلًا فوريًا وأداء فائقًا بدون استهلاك لذاكرة الجهاز.
5. **بيان طريقة الفحص البصري:**
   > [!IMPORTANT]
   > يُعلن التقرير بشفافية ونزاهة أن مراجعة الرسومات تمت **برمجيًا وثابتًا (Static & Programmatic Verification)** عبر فحص وسوم المتجهات والتدرجات والمسارات، واختبار العرض في بيئة Headless Browser في جناحي `phase5b1_1` و `phase5b1_2`. لم يتم فتح عارض نوافذ مرئي تفاعلي (Interactive Desktop GUI) في جلسة الطرفية الحالية، ولذلك لا ندّعي اجتياز فحص بصري يدوي لم يحدث.

---

## 4. مسارات العرض والكاش في الواجهة الحالية

1. **آلية بطاقات التمارين (`renderExercises`):**
   - ترث بطاقات التمارين وروتينات القوالب الصورة الافتراضية عبر `transformTemplateExerciseToRuntime` من `cat.images[0]`.
   - يتحقق كود العرض من أسبقية صورة المستخدم المخصصة عبر `getExerciseImageRecord(ex.key)`.
   - عند وجود صورة مخصصة في IndexedDB، تُعرض فورًا وتطغى على الرسم الافتراضي.
   - عند غياب صورة المستخدم، يُعرض رسم الـ SVG الافتراضي المحلي دون أي اتصال بالإنترنت.
2. **آلية موسوعة التمارين الرياضية (`renderEncyclopediaDetailHtml`):**
   - أصبحت الموسوعة تعرض الرسم التوضيحي عالي الدقة داخل بطاقة تفاصيل التمرين عبر `encImgSrc`.
   - عند إضافة تمرين من الموسوعة لبرنامج المستخدم عبر `encConfirmAddBtn`، يتم حفظ مسار الرسم تلقائيًا مع التمرين المخصص الجديد (`img: selectedEx.images[0]`).
3. **كاش الخدمة في `sw.js`:**
   - إصدار الكاش: **`v24`** (`CACHE_VERSION = 'v24'`).
   - قائمة `SHELL_ASSETS`: تضم **95 أصلًا محليًا** (منها 31 رسم SVG لتمارين الجيم).
   - تم التحقق من وجود جميع ملفات `SHELL_ASSETS` الـ 95 على القرص بدون أي مرجع مكسور.

---

## 5. مصفوفة التغطية الراهنة والتصنيف الخماسي الدقيق

بعد تنفيذ Phase 12.1B وربط الرسوم بالكتالوج، تمت إعادة تصنيف جميع تمارين الكتالوج الـ 119:

```mermaid
pie title توزيع تغطية كتالوج تمارين Zatoona بعد Phase 12.1B (119 تمرينًا)
    "D — Covered (30)" : 30
    "A — Missing (82)" : 82
    "E — Needs Review (7)" : 7
    "B — Invalid (0)" : 0
    "C — Mismatch (0)" : 0
```

### مقارنة التغطية قبل وبعد Phase 12.1B:

| الفئة الصارمة | الوصف الفني | العدد في Phase 12.1A (السابق) | العدد في Phase 12.1C (الحالي) | التغير |
|:---:|---|:---:|:---:|:---:|
| **D** | `Covered` — مغطى برسم محلي مطابق وصالح | 11 | **30** | **+19** |
| **E** | `Needs Review` — تشابه جزئي يحتاج مراجعة | 8 | **7** | **-1** (`seated_db_press` حُسم) |
| **A** | `Missing` — لا توجد صورة افتراضية ملحقة | 100 | **82** | **-18** (تم رسمها وربطها) |
| **B** | `Invalid` — مرجع مفقود أو مكسور | 0 | **0** | ثابت |
| **C** | `Mismatch` — صورة غير مطابقة للتمرين | 0 | **0** | ثابت |
| **المجموع** | | **119** | **119** | تطابق تام 100% |

### حالة تغطية قوالب الجيم الجاهزة الـ 4 (`GYM_PLAN_TEMPLATE_REGISTRY`):

- **إجمالي التمارين الفريدة في القوالب:** **26 تمرينًا**.
- **المغطى برسم مطابق في الكتالوج:** **26 تمرينًا (100.0%)**.
  * 19 تمرينًا غُطيت برسومات جديدة أُنشئت في Phase 12.1B.
  * 7 تمارين غُطيت برسومات كلاسيكية سابقة مطابقة تمامًا.
- **النتيجة المثبتة بالأدلة:** **لا يوجد أي تمرين واحد داخل قوالب الجيم الجاهزة يظهر بصندوق رمادي فارغ `.no-photo` لدى أي مستخدم جديد للتطبيق**.

---

## 6. قائمة الأولويات المقترحة للدفعة التالية (Phase 12.1D Priorities)

انطلاقًا من التمارين الـ 89 المتبقية دون صور (82 في الفئة A و 7 في الفئة E)، تم فرز وتحديد قائمة تضم **20 تمرينًا ذا أولوية قصوى** للدفعة القادمة، مرتبة وفق المعايير الإلزامية:

1. **التمارين المركبة الأساسية المتبقية (15 تمرينًا):**
   - `barbell_front_squat` (السكوات الأمامي بالبار): تمرين الأرجل المركب الأكثر طلبًا لعزل الفخذ الأمامي؛ يختلف عن السكوات الخلفي بحمل البار على الكتف الأمامي والترقوة واستقامة الجذع.
   - `chest_dips` (المتوازي للصدر): تمرين وزن جسم مركب أساسي لعضلات الصدر السفلية؛ يتميز بميل الجذع للأمام 30° وفتح الكوعين.
   - `one_arm_dumbbell_row` (تجديف دمبل فردي / منشار): التمرين الأحادي الأكثر شعبية للظهر والمجنص؛ وضع ركبة ويد على البنش.
   - `t_bar_row` (تجديف تي بار): تمرين الظهر الأوسط الأساسي لبناء الكثافة العضلية.
   - `barbell_hip_thrust` (هيب ثرست بالبار): الحركة المركبة الأساسية لعضلات المؤخرة (Glutes) مع استناد الظهر العلوي على البنش.
   - `bulgarian_split_squat` (بلغاريان سبليت سكوات بالدمبل): تمرين الأرجل الأحادي الذهبي للأماميات والخلفيات مع رفع القدم الخلفية على بنش.
   - `sumo_deadlift` (سومو ديدليفت بالبار): الرفعة البديلة الكلاسيكية للديدليفت؛ وقفة واسعة جدًا وقبضة داخل الفخذين.
   - `hack_squat_machine` (هاك سكوات بالماكينة): ماكينة السكوات الأساسية في الصالات الرياضية ذات مسار مائل 45°.
   - `pendlay_row` (بيندلاي رو بالبار): تجديف ظهر بالبار أفقي صارم يعود فيه البار للمس الأرض في كل تكرار.
   - `close_grip_bench_press` (بنش قبضة ضيقة بالبار): حركة مركبة رئيسية للترايسبس؛ مسافة القبضة بعرض الكتفين.
   - `arnold_press` (أرنولد برس بالدمبل جالس): تمرين الكتف الكلاسيكي الشهير الذي يدور فيه الكف 180° أثناء الضغط.
   - `kettlebell_swing` (سوينج كيتل بيل): حركة مرجحة ديناميكية متفجرة للسلسلة الخلفية والأوراك.
   - `ab_wheel_rollout` (دحرجة عجلة البطن): أقوى حركة مركبة ديناميكية للجذع والبطن.
   - `farmers_walk` (مشي المزارع بالدمبل): حركة وظيفية مركبة لقوة القبضة والساعدين والترابيس والجذع.
   - `chin_up` (عقلة قبضة سفلية معكوسة): حركة وزن جسم مركبة للبايسبس والمجنص؛ تختلف جوهريًا عن `pull_up` في توجيه الكفين للداخل.

2. **تمارين شائعة مكملة للموسوعة (5 تمارين):**
   - `decline_barbell_bench_press` (بنش هابط بالبار): حركة مركبة لاستهداف زاوية الصدر السفلي.
   - `cable_crossover_high_to_low` (تجميع كابل من أعلى لأسفل): حركة عزل أساسية للصدر على جهاز الكابل المزدوج.
   - `preacher_curl` (كيرل بايسبس على بنش بريتشر / لاري سكوت): حركة عزل البايسبس الأكثر انتشارًا على مسند مائل ببار EZ.
   - `cable_kneeling_crunch` (كرانش كابل راكعاً): تمرين البطن الأساسي بالكابل (سجود بالكابل).
   - `dumbbell_shrugs` (شراجز بالدمبل / هز الأكتاف): تمرين الترابيس والرقبة الأكثر استخدامًا بالدمبل.

### جدول تفاصيل الـ 20 تمرينًا المقترحة لـ Phase 12.1D:

| # | معرّف التمرين (Catalog ID) | الاسم بالعربية | نوع الحركة | المعدات | سبب الأولوية الفنية |
|:---:|---|---|:---:|:---:|---|
| 1 | `barbell_front_squat` | سكوات أمامي بالبار | مركب | بار | تمرين كلاسيكي أساسي؛ يختلف عن السكوات الخلفي بالمسار واستقامة الجذع |
| 2 | `chest_dips` | متوازي للصدر (Dips) | مركب | وزن الجسم | حركة وزن جسم أساسية؛ تختلف عن غطس الترايسبس بميل الصدر للأمام |
| 3 | `one_arm_dumbbell_row` | تجديف دمبل فردي (منشار) | مركب | دمبل | الحركة الأحادية الأكثر انتشارًا للظهر؛ وضوح وضعية البنش والركبة |
| 4 | `t_bar_row` | تجديف تي بار | مركب | بار | حركة الظهر الوسطى الأساسية؛ مقبض V مائل للصدر |
| 5 | `barbell_hip_thrust` | هيب ثرست بالبار | مركب | بار | الحركة الذهبية لعضلات الحوض والمؤخرة؛ لا يوجد بديل يماثلها حالياً |
| 6 | `bulgarian_split_squat` | بلغاريان سبليت سكوات | مركب | دمبل | تمرين أحادي عالي الفعالية؛ القدم الخلفية مرتفعة على البنش |
| 7 | `sumo_deadlift` | سومو ديدليفت بالبار | مركب | بار | بديل الديدليفت الكلاسيكي؛ فتحة قدمين واسعة جدًا |
| 8 | `hack_squat_machine` | هاك سكوات بالماكينة | مركب | ماكينة | ماكينة الأرجل الأساسية في كل صالة؛ مسند مائل ووسائد كتف |
| 9 | `pendlay_row` | بيندلاي رو بالبار | مركب | بار | تجديف صارم يبدأ من الثبات على الأرض بزاوية 90° |
| 10 | `close_grip_bench_press` | بنش برس قبضة ضيقة | مركب | بار | حركة ترايسبس مركبة؛ تختلف عن البنش العادي بضيق المسافة |
| 11 | `arnold_press` | أرنولد برس بالدمبل جالس | مركب | دمبل | حركة دوران الكف 180° لضرب الرؤوس الثلاثة للكتف |
| 12 | `kettlebell_swing` | سوينج كيتل بيل | مركب | كيتل بيل | الحركة الوظيفية الأكثر شهرة في الكتالوج لأدوات الكيتل بيل |
| 13 | `ab_wheel_rollout` | دحرجة عجلة البطن | مركب | أخرى | الحركة الأعلى فعالية في تنشيط عضلات الجذع بالكامل |
| 14 | `farmers_walk` | مشي المزارع بالدمبل | مركب | دمبل | حركة مشي حاملة للأوزان لبناء القبضة والترابيس والجذع |
| 15 | `chin_up` | عقلة قبضة سفلية معكوسة | مركب | وزن الجسم | حركة مركبة رئيسية؛ تختلف تشريحيًا وحركيًا عن `pull_up` |
| 16 | `decline_barbell_bench_press` | بنش هابط بالبار | مركب | بار | استكمال زوايا الصدر الثلاث (مستوي، مائل، هابط) بالبار |
| 17 | `cable_crossover_high_to_low` | تجميع كابل من أعلى لأسفل | عزل | كابل | حركة كابل الصدر الأكثر شيوعًا لعزل الألياف السفلية |
| 18 | `preacher_curl` | كيرل بار بريتشر (لاري سكوت) | عزل | بار | أشهر حركة عزل للبايسبس؛ مسند الذراعين المائل يمنع الغش |
| 19 | `cable_kneeling_crunch` | كرانش كابل راكعاً (سجود) | عزل | كابل | تمرين البطن الأكثر استخدامًا على أجهزة الكابل مع المقاومة |
| 20 | `dumbbell_shrugs` | رفع الكتفين بالدمبل (ترابيس) | عزل | دمبل | تمرين الترابيس والرقبة الأكثر كفاءة وشهرة بالدمبل |

---

## 7. فحص المشكلات المكتشفة والحلول المحققة

1. **حالة اختبار Phase 9C.1 وتحديث الكاش:**
   - تم التحقق من أن فحص `test_phase9c1_stretch_encyclopedia.py` يجتاز بنجاح تام بعد تحديث تعليق الكاش المرجعي في `sw.js` دون أي تراجع في الإصدار الفعلي `v24`.
2. **عدم وجود أي أصول مكسورة أو مفقودة:**
   - جميع أصول `SHELL_ASSETS` الـ 95 موجودة وصالحة وتعمل دون إنترنت.
3. **تطابق البيئة وملفات العرض:**
   - ملف `zatoona.html` يطابق `index.html` تطابقًا ثنائيًا مطلقًا.

---

## 8. جدول التغطية الكامل لجميع تمارين الكتالوج الـ 119

يوضح الجدول المرجعي التالي الحالة الدقيقة لكل تمرين من التمارين الـ 119 في الكتالوج بعد إتمام Phase 12.1B:

| # | معرّف التمرين (ID) | الاسم بالعربية | الاسم بالإنجليزية | العضلة | النوع | المعدات | القالب | الفئة | رسم الـ SVG / الملاحظة | مرحلة التغطية |
|---|---|---|---|---|---|---|:---:|:---:|---|:---:|
| 1 | `barbell_bench_press` | بنش برس بالبار مستوي | Barbell Bench Press | chest | compound | barbell | ✓ | **D** | `ex-a02-bench-press.svg` | Pre-12.1B (قديم) |
| 2 | `incline_barbell_bench_press` | بنش مائل عالي بالبار | Incline Barbell Bench Press | chest | compound | barbell | ✓ | **D** | `ex-incline-barbell-bench-press.svg` | Phase 12.1B (جديد) |
| 3 | `decline_barbell_bench_press` | بنش هابط بالبار | Decline Barbell Bench Press | chest | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 4 | `dumbbell_bench_press` | بنش برس بالدمبل مستوي | Dumbbell Bench Press | chest | compound | dumbbell | ✓ | **D** | `ex-dumbbell-bench-press.svg` | Phase 12.1B (جديد) |
| 5 | `incline_dumbbell_press` | بنش مائل عالي بالدمبل | Incline Dumbbell Press | chest | compound | dumbbell | ✓ | **D** | `ex-incline-dumbbell-press.svg` | Phase 12.1B (جديد) |
| 6 | `decline_dumbbell_press` | بنش هابط بالدمبل | Decline Dumbbell Press | chest | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 7 | `dumbbell_chest_flyes` | تجميع دمبل مستوي (تفتيح صدر) | Dumbbell Chest Flyes | chest | isolation | dumbbell | ✓ | **D** | `ex-dumbbell-chest-flyes.svg` | Phase 12.1B (جديد) |
| 8 | `incline_dumbbell_flyes` | تجميع دمبل على بنش مائل عالي | Incline Dumbbell Flyes | chest | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 9 | `cable_crossover_high_to_low` | تجميع كابل من أعلى لأسفل | Cable Crossover (High to Low) | chest | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 10 | `cable_crossover_low_to_high` | تجميع كابل من أسفل لأعلى | Low Cable Crossover | chest | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 11 | `chest_dips` | متوازي للصدر (Dips) | Chest Dips | chest | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 12 | `push_up` | تمرين الضغط الكلاسيكي | Standard Push-Up | chest | compound | bodyweight | — | **D** | `ex-b03-push-up.svg` | Pre-12.1B (قديم) |
| 13 | `diamond_push_up` | تمرين الضغط الماسي | Diamond Push-Up | chest, triceps | compound | bodyweight | — | **E** | تشابه جزئي مع `ex-b03-push-up.svg` (ضغط ماسي vs قياسي) | — |
| 14 | `machine_chest_press` | دفع الصدر بالماكينة جالس | Machine Chest Press | chest | compound | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 15 | `pec_deck_fly` | تجميع الصدر بالماكينة (بيليفاي / بيك ديك) | Pec Deck Machine Fly | chest | isolation | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 16 | `conventional_deadlift` | الرفعة الميتة كلاسيكي بالبار (ديدليفت) | Barbell Conventional Deadlift | lower_back, hamstrings, glutes | compound | barbell | ✓ | **D** | `ex-conventional-deadlift.svg` | Phase 12.1B (جديد) |
| 17 | `barbell_bent_over_row` | تجديف بالبار مائل (بار سحب ظهر) | Barbell Bent-Over Row | lats, back | compound | barbell | ✓ | **D** | `ex-b02-barbell-row.svg` | Pre-12.1B (قديم) |
| 18 | `pendlay_row` | بيندلاي رو بالبار (تجديف من الأرض) | Pendlay Row | back, lats | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 19 | `t_bar_row` | تجديف تي بار (T-Bar Row) | T-Bar Row | back, lats | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 20 | `one_arm_dumbbell_row` | تجديف دمبل فردي (منشار دمبل) | One-Arm Dumbbell Row | lats, back | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 21 | `lat_pulldown_wide_grip` | سحب عالي بالماكينة قبضة واسعة | Lat Pulldown (Wide Grip) | lats | compound | machine | ✓ | **D** | `ex-a03-lat-pulldown.svg` | Pre-12.1B (قديم) |
| 22 | `lat_pulldown_close_grip` | سحب عالي قبضة ضيقة محايدة (V-Bar) | Close-Grip Lat Pulldown | lats | compound | machine | — | **E** | تشابه جزئي مع `ex-a03-lat-pulldown.svg` (سحب عالي قبضة ضيقة vs واسعة) | — |
| 23 | `seated_cable_row` | تجديف كابل جالس (سحب أرضي) | Seated Cable Row | back, lats | compound | cable | ✓ | **D** | `ex-seated-cable-row.svg` | Phase 12.1B (جديد) |
| 24 | `straight_arm_cable_pulldown` | سحب كابل بذراعين مفرودتين (عزل لاتس) | Straight-Arm Cable Pulldown | lats | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 25 | `pull_up` | تمرين العقلة قبضة علوية واسعة | Pull-Up | lats, back | compound | bodyweight | — | **D** | `ex-b04-pull-up.svg` | Pre-12.1B (قديم) |
| 26 | `chin_up` | تمرين العقلة قبضة سفلية معكوسة | Chin-Up | lats, biceps | compound | bodyweight | — | **E** | تشابه جزئي مع `ex-b04-pull-up.svg` (عقلة قبضة سفلية vs علوية) | — |
| 27 | `inverted_row` | تجديف عكسي بوزن الجسم (أستراليان رو) | Inverted Row (Bodyweight) | back, lats | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 28 | `dumbbell_pullover` | بول أوفر بالدمبل نائم | Dumbbell Pullover | lats, chest | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 29 | `back_extensions` | فرد الظهر على المقعد الروماني (هايبر اكستنشن) | Hyperextensions (Back Extension) | lower_back | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 30 | `machine_seated_row` | تجديف ظهر جالس بالماكينة | Machine Seated Row | back, lats | compound | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 31 | `standing_overhead_barbell_press` | ضغط أوفرهيد بالبار واقف (الضغط العسكري) | Standing Overhead Barbell Press | shoulders | compound | barbell | ✓ | **D** | `ex-a04-overhead-press.svg` | Pre-12.1B (قديم) |
| 32 | `seated_dumbbell_shoulder_press` | شولدر برس بالدمبل جالس | Seated Dumbbell Shoulder Press | shoulders | compound | dumbbell | ✓ | **D** | `ex-seated-dumbbell-shoulder-press.svg` | Phase 12.1B (جديد) |
| 33 | `arnold_press` | أرنولد برس بالدمبل جالس | Arnold Press | shoulders | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 34 | `standing_dumbbell_lateral_raise` | رفرفة كتف جانبي بالدمبل واقف | Standing Dumbbell Lateral Raise | shoulders | isolation | dumbbell | ✓ | **D** | `ex-standing-dumbbell-lateral-raise.svg` | Phase 12.1B (جديد) |
| 35 | `seated_dumbbell_lateral_raise` | رفرفة كتف جانبي بالدمبل جالس | Seated Dumbbell Lateral Raise | shoulders | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 36 | `cable_lateral_raise` | رفرفة كتف جانبي بالكابل فردي | Cable Lateral Raise | shoulders | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 37 | `front_dumbbell_raise` | رفرفة كتف أمامي بالدمبل | Front Dumbbell Raise | shoulders | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 38 | `face_pull_cable` | فيس بول بالحبل على الكابل (سحب للوجه) | Face Pull with Rope | shoulders, traps | compound | cable | ✓ | **D** | `ex-a06-face-pull.svg` | Pre-12.1B (قديم) |
| 39 | `rear_delt_dumbbell_fly` | رفرفة كتف خلفي بالدمبل مائل | Rear Delt Dumbbell Fly (Bent-Over) | shoulders | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 40 | `reverse_pec_deck` | كتف خلفي بالماكينة (فراشة مقلوبة) | Reverse Pec Deck Fly | shoulders | isolation | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 41 | `barbell_upright_row` | سحب بار للأعلى للكتف والترابيس (أب رايت رو) | Barbell Upright Row | shoulders, traps | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 42 | `barbell_shrugs` | رفع الكتفين بالبار (ترابيس بالبار) | Barbell Shrugs | traps | isolation | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 43 | `dumbbell_shrugs` | رفع الكتفين بالدمبل (ترابيس بالدمبل) | Dumbbell Shrugs | traps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 44 | `barbell_curl` | كيرل بايسبس بالبار مستقيم واقف | Standing Barbell Bicep Curl | biceps | isolation | barbell | ✓ | **D** | `ex-barbell-curl.svg` | Phase 12.1B (جديد) |
| 45 | `ez_bar_bicep_curl` | كيرل بايسبس بالبار المتعرج (EZ-Bar) | EZ-Bar Bicep Curl | biceps | isolation | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 46 | `alternating_dumbbell_curl` | كيرل دمبل تبادلي واقف (تبادل دمبل باي) | Alternating Dumbbell Bicep Curl | biceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 47 | `incline_dumbbell_curl` | كيرل دمبل على بنش مائل (إطالة الرأس الطويل) | Incline Dumbbell Bicep Curl | biceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 48 | `hammer_curl` | كيرل شاكوش بالدمبل (هامر كيرل) | Dumbbell Hammer Curl | biceps, forearms | isolation | dumbbell | ✓ | **D** | `ex-hammer-curl.svg` | Phase 12.1B (جديد) |
| 49 | `cable_rope_hammer_curl` | كيرل هامر بالحبل على الكابل | Cable Rope Hammer Curl | biceps, forearms | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 50 | `preacher_curl` | كيرل بار بريتشر على مسند الواعظ (لاري سكوت) | Preacher Curl (EZ-Bar) | biceps | isolation | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 51 | `concentration_curl` | كيرل تركيز بالدمبل جالس (كونسنتريشن) | Concentration Curl | biceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 52 | `standing_cable_curl` | كيرل بايسبس بالكابل واقف بالمسطرة | Standing Cable Bicep Curl | biceps | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 53 | `triceps_rope_pushdown` | ترايسبس كابل دفع لأسفل بالحبل | Cable Rope Triceps Pushdown | triceps | isolation | cable | ✓ | **D** | `ex-triceps-rope-pushdown.svg` | Phase 12.1B (جديد) |
| 54 | `triceps_bar_pushdown` | ترايسبس كابل دفع لأسفل بالمسطرة (أو بار V) | Cable Bar Triceps Pushdown | triceps | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 55 | `skull_crushers` | فرنساوي بار EZ نائم على البنش (سكل كراشر) | EZ-Bar Skull Crushers (Lying Triceps Extension) | triceps | isolation | barbell | ✓ | **D** | `ex-skull-crushers.svg` | Phase 12.1B (جديد) |
| 56 | `overhead_dumbbell_triceps_extension` | فرنساوي دمبل خلف الرأس جالس (أوفرهيد) | Overhead Dumbbell Triceps Extension | triceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 57 | `overhead_cable_triceps_extension` | ترايسبس كابل علوي فوق الرأس بالحبل | Overhead Cable Triceps Extension | triceps | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 58 | `close_grip_bench_press` | بنش برس قبضة ضيقة بالبار (تركيز ترايسبس) | Close-Grip Barbell Bench Press | triceps, chest | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 59 | `parallel_bar_triceps_dips` | غطس متوازي للترايسبس (Dips عمودي) | Triceps Dips on Parallel Bars | triceps | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 60 | `bench_dips` | غطس الترايسبس على حافة البنش | Bench Dips | triceps | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 61 | `dumbbell_kickback` | كيك باك بالدمبل للترايسبس | Dumbbell Triceps Kickback | triceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 62 | `barbell_back_squat` | سكوات خلفي بالبار (القرفصاء بالبار) | Barbell Back Squat | quads | compound | barbell | ✓ | **D** | `ex-barbell-back-squat.svg` | Phase 12.1B (جديد) |
| 63 | `barbell_front_squat` | سكوات أمامي بالبار (فرونت سكوات) | Barbell Front Squat | quads | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 64 | `goblet_squat` | سكوات جوبلت بالدمبل (Goblet Squat) | Goblet Squat with Dumbbell | quads | compound | dumbbell | — | **D** | `ex-a01-goblet-squat.svg` | Pre-12.1B (قديم) |
| 65 | `leg_press` | مكبس الأرجل بزاوية 45 درجة (ليج برس) | 45-Degree Leg Press Machine | quads | compound | machine | ✓ | **D** | `ex-leg-press.svg` | Phase 12.1B (جديد) |
| 66 | `hack_squat_machine` | هاك سكوات بالماكينة | Hack Squat Machine | quads | compound | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 67 | `bulgarian_split_squat` | بلغاريان سبليت سكوات بالدمبل (سكوات بلغاري) | Bulgarian Split Squat with Dumbbells | quads, glutes | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 68 | `walking_lunges_dumbbell` | طعنات مشي بالدمبل (لانجز مشي) | Dumbbell Walking Lunges | quads, glutes | compound | dumbbell | — | **D** | `ex-b06-lunges.svg` | Pre-12.1B (قديم) |
| 69 | `leg_extension_machine` | فرد أرجل أمامي بالماكينة (ليج اكستنشن) | Leg Extension Machine | quads | isolation | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 70 | `step_ups_dumbbell` | صعود المنصة بالدمبل (ستيب أب) | Dumbbell Step-Ups | quads, glutes | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 71 | `romanian_deadlift_barbell` | ديدليفت روماني بالبار (RDL) | Barbell Romanian Deadlift (RDL) | hamstrings, glutes | compound | barbell | ✓ | **D** | `ex-b01-romanian-deadlift.svg` | Pre-12.1B (قديم) |
| 72 | `romanian_deadlift_dumbbell` | ديدليفت روماني بالدمبل (RDL دمبل) | Dumbbell Romanian Deadlift | hamstrings, glutes | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 73 | `lying_leg_curl_machine` | ثني أرجل خلفي نائم بالماكينة (ليج كيرل نائم) | Lying Leg Curl Machine | hamstrings | isolation | machine | ✓ | **D** | `ex-lying-leg-curl-machine.svg` | Phase 12.1B (جديد) |
| 74 | `seated_leg_curl_machine` | ثني أرجل خلفي جالس بالماكينة (ليج كيرل جالس) | Seated Leg Curl Machine | hamstrings | isolation | machine | ✓ | **D** | `ex-seated-leg-curl-machine.svg` | Phase 12.1B (جديد) |
| 75 | `barbell_hip_thrust` | هيب ثرست بالبار (Hip Thrust) | Barbell Hip Thrust | glutes | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 76 | `cable_glute_kickback` | كيك باك للمؤخرة بالكابل (Glute Kickback) | Cable Glute Kickback | glutes | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 77 | `kettlebell_swing` | سوينج كيتل بيل (مرجحة الكيتل بيل) | Kettlebell Swing | glutes, hamstrings | compound | kettlebell | — | **A** | لا يوجد رسم افتراضي | — |
| 78 | `sumo_deadlift` | سومو ديدليفت بالبار (وقفة واسعة) | Barbell Sumo Deadlift | glutes, hamstrings, quads | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 79 | `standing_calf_raise_machine` | رفع سمانة واقف بالماكينة | Standing Calf Raise Machine | calves | isolation | machine | ✓ | **D** | `ex-standing-calf-raise-machine.svg` | Phase 12.1B (جديد) |
| 80 | `seated_calf_raise_machine` | رفع سمانة جالس بالماكينة (تركيز العضلة النعلية) | Seated Calf Raise Machine | calves | isolation | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 81 | `single_leg_dumbbell_calf_raise` | رفع سمانة رجل واحدة بالدمبل | Single-Leg Dumbbell Calf Raise | calves | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 82 | `leg_press_calf_raise` | رفع سمانة على جهاز مكبس الأرجل | Leg Press Calf Raise (Calf Press) | calves | isolation | machine | — | **A** | لا يوجد رسم افتراضي | — |
| 83 | `plank` | تمرين البلانك الثابت (لوح الخشب) | Front Plank | abs | isolation | bodyweight | ✓ | **D** | `ex-a05-plank.svg` | Pre-12.1B (قديم) |
| 84 | `side_plank` | البلانك الجانبي (ثبات لعضلات الخصر) | Side Plank | abs | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 85 | `hanging_leg_raise` | رفع الأرجل في وضع التعليق على العقلة | Hanging Leg Raise | abs | compound | bodyweight | ✓ | **D** | `ex-hanging-leg-raise.svg` | Phase 12.1B (جديد) |
| 86 | `hanging_knee_raise` | رفع الركبتين تعليقاً على العقلة | Hanging Knee Raise | abs | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 87 | `cable_kneeling_crunch` | كرانش البطن بالكابل راكعاً (سجود بالكابل) | Kneeling Cable Crunch | abs | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 88 | `ab_wheel_rollout` | دحرجة عجلة البطن (آب رول آوت) | Ab Wheel Rollout | abs | compound | other | — | **A** | لا يوجد رسم افتراضي | — |
| 89 | `russian_twists` | التدوير الروسي لعضلات الخصر (Russian Twist) | Russian Twist | abs | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 90 | `seated_palms_up_wrist_curl` | ثني رسغ بالبار جالس كف لأعلى (ساعد داخلي) | Seated Palms-Up Barbell Wrist Curl | forearms | isolation | barbell | ✓ | **D** | `ex-seated-palms-up-wrist-curl.svg` | Phase 12.1B (جديد) |
| 91 | `seated_palms_down_wrist_curl` | مد رسغ بالبار جالس كف لأسفل (ساعد خارجي) | Seated Palms-Down Barbell Wrist Curl | forearms | isolation | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 92 | `farmers_walk` | مشي المزارع بالدمبل (فارمرز ووك) | Dumbbell Farmer's Walk | forearms, traps | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 93 | `dead_hang` | التعلق الميت على عقلة (ديد هانج لقوة القبضة والكتف) | Dead Hang on Pull-Up Bar | forearms | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 94 | `band_pull_apart` | سحب شريط المقاومة أفقي (باند بول أبارت) | Resistance Band Pull-Apart | shoulders, traps | isolation | bands | — | **A** | لا يوجد رسم افتراضي | — |
| 95 | `band_bicep_curl` | كيرل بايسبس بشريط المقاومة | Resistance Band Bicep Curl | biceps | isolation | bands | — | **A** | لا يوجد رسم افتراضي | — |
| 96 | `band_triceps_pushdown` | دفع ترايسبس بشريط المقاومة | Resistance Band Triceps Pushdown | triceps | isolation | bands | — | **A** | لا يوجد رسم افتراضي | — |
| 97 | `band_monster_walk` | مشي جانبي بشريط المقاومة للمؤخرة (مونستر ووك) | Band Monster Walk (Lateral Walk) | glutes | isolation | bands | — | **A** | لا يوجد رسم افتراضي | — |
| 98 | `band_face_pull` | فيس بول بشريط المقاومة (سحب للوجه بالباند) | Resistance Band Face Pull | shoulders, traps | compound | bands | — | **A** | لا يوجد رسم افتراضي | — |
| 99 | `kettlebell_goblet_squat` | جوبلت سكوات بالكيتل بيل | Kettlebell Goblet Squat | quads | compound | kettlebell | — | **E** | تشابه جزئي مع `ex-a01-goblet-squat.svg` (كوب سكوات دمبل vs كيتل بيل) | — |
| 100 | `kettlebell_deadlift` | الرفعة الميتة بالكيتل بيل (ديدليفت) | Kettlebell Deadlift | glutes, hamstrings, lower_back | compound | kettlebell | — | **A** | لا يوجد رسم افتراضي | — |
| 101 | `kettlebell_overhead_press` | ضغط كتف فردي بالكيتل بيل | Single-Arm Kettlebell Overhead Press | shoulders | compound | kettlebell | — | **A** | لا يوجد رسم افتراضي | — |
| 102 | `kettlebell_turkish_get_up` | النهوض التركي بالكيتل بيل (تركيش جيت أب) | Turkish Get-Up with Kettlebell | abs, shoulders | compound | kettlebell | — | **A** | لا يوجد رسم افتراضي | — |
| 103 | `decline_push_up` | تمرين الضغط بقدمين مرتفعتين (استهداف الصدر العلوي) | Decline Push-Up (Feet Elevated) | chest, shoulders | compound | bodyweight | — | **E** | تشابه جزئي مع `ex-b03-push-up.svg` (ضغط قدمين مرتفعتين vs قياسي) | — |
| 104 | `incline_push_up` | تمرين الضغط بيدين مرتفعتين (مبتدئ / صدر سفلي) | Incline Push-Up (Hands Elevated) | chest | compound | bodyweight | — | **E** | تشابه جزئي مع `ex-b03-push-up.svg` (ضغط يدين مرتفعتين vs قياسي) | — |
| 105 | `barbell_good_morning` | جود مورنينجز بالبار (انحناء صباح الخير للظهر والخلفيات) | Barbell Good Mornings | lower_back, hamstrings | compound | barbell | — | **A** | لا يوجد رسم افتراضي | — |
| 106 | `single_arm_cable_lat_pulldown` | سحب عالي كابل فردي بذراع واحدة | Single-Arm Cable Lat Pulldown | lats | compound | cable | — | **E** | تشابه جزئي مع `ex-a03-lat-pulldown.svg` (سحب كابل فردي vs ماكينة ثنائي) | — |
| 107 | `chest_supported_dumbbell_row` | تجديف بالدمبل مسنود الصدر على بنش مائل (سيل رو) | Chest-Supported Dumbbell Row (Incline) | back, lats | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 108 | `spider_curl` | سبايدر كيرل بالدمبل على بنش مائل (عزل البايسبس) | Spider Curl (Incline Bench Bicep Curl) | biceps | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 109 | `zottman_curl` | زوتمان كيرل بالدمبل (للبايسبس والساعد معاً) | Zottman Bicep Curl | biceps, forearms | isolation | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 110 | `cable_single_arm_pushdown` | دفع ترايسبس كابل بذراع واحدة | Single-Arm Cable Triceps Pushdown | triceps | isolation | cable | — | **A** | لا يوجد رسم افتراضي | — |
| 111 | `sissy_squat_bodyweight` | سيسي سكوات بوزن الجسم (عزل عضلات الفخذ الأمامية) | Bodyweight Sissy Squat | quads | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 112 | `box_jump` | القفز على الصندوق (بوكس جمب بليومترك) | Plyometric Box Jump | quads, glutes, calves | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 113 | `bodyweight_glute_bridge` | جلوت بريدج بوزن الجسم على الأرض (جسر الحوض) | Bodyweight Glute Bridge | glutes | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 114 | `single_leg_dumbbell_rdl` | ديدليفت روماني ساق واحدة بالدمبل (توازن وخلفيات) | Single-Leg Dumbbell Romanian Deadlift | hamstrings, glutes | compound | dumbbell | — | **A** | لا يوجد رسم افتراضي | — |
| 115 | `bodyweight_calf_raise` | رفع سمانة واقف بوزن الجسم | Standing Bodyweight Calf Raise | calves | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 116 | `bicycle_crunch` | كرانشز الدراجة الهوائية للبطن والجوانب | Bicycle Crunch | abs | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 117 | `dead_bug` | تمرين الحشرة الميتة (ديد باج لثبات الكور) | Dead Bug Exercise | abs | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 118 | `bird_dog` | تمرين بيرد دوج (Bird Dog لتوازن العمود الفقري والكور) | Bird Dog Exercise | abs, lower_back | isolation | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |
| 119 | `mountain_climbers` | تمرين تسلق الجبال (ماونتن كلايمبرز) | Mountain Climbers | abs | compound | bodyweight | — | **A** | لا يوجد رسم افتراضي | — |

---
*نهاية تقرير التدقيق الفني Phase 12.1C — Zatoona Post-Implementation Coverage Reconciliation*
