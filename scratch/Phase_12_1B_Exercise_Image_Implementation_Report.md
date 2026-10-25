# تقرير تنفيذ صور كتالوج التمارين الرياضية (Phase 12.1B)
## Curated Exercise Catalog Images — Offline-First SVG Implementation

- **المشروع:** Zatoona (تطبيق ويب تقدمي شخصي Offline-First PWA)
- **المسار المحلي:** `<REPOSITORY_ROOT>`
- **تاريخ وساعة التنفيذ:** 2026-10-25T17:15:00+03:00
- **نوع المهمة:** تنفيذ رسومات SVG أصلية ومحلية وسد فجوات صور القوالب الجاهزة بنسبة 100%
- **حالة بوابة الانحدار:** **PASS ✅ — 10 أجنحة من أصل 10 (540 / 540 فحصًا ناجحًا بنسبة 100%)**

---

## 1. ملخص الإنجاز والعدد الفعلي للرسومات الجديدة

تم إنشاء **19 رسم SVG أصلي ومحلي جديد** داخل المجلد `assets/images/exercises/`، مخصصة لتمارين القوالب الجاهزة الأساسية (Tier 1 و Tier 2). تم تصميم كل رسم يدويًا كملف متجهي خفيف (Pure Vector SVG) يلتزم بدقة بالسياسة البصرية المعتمدة في المشروع:
- **رجال بالغون فقط (Adult Males Only)** في جميع الوضعيات والحركات.
- أسلوب بصري موحد يطابق الرسوم الاثني عشر السابقة (`viewBox="0 0 300 200"`، خلفية منحنية الحواف، خط أرضية، شارة تعريفية، أسهم حركية برتقالية `#e65100`، ونقاط تركيز عضلي).
- تمايز واضح بين المعدات (بار vs دمبل vs كابل vs ماكينة) والوضعيات (مستوي vs مائل vs جالس vs واقف vs نائم).
- أحجام خفيفة للغاية تتراوح بين **2.3 و 3.3 كيلوبايت** لكل ملف، بدون أي صور نقطية Base64 أو سكربتات أو خطوط خارجية.

### قائمة ملفات الـ SVG الـ 19 الجديدة وأحجامها:

| # | معرّف التمرين (ID) | اسم ملف الرسم الجديد | الحجم (بايت) | الفئة | المعدات والوضعية |
|:---:|---|---|:---:|:---:|---|
| 1 | `barbell_back_squat` | `ex-barbell-back-squat.svg` | 3,333 | Tier 1 (مركب) | بار أولمبي محمول على الترابيس، قرفصاء عميقة موازية للأرض |
| 2 | `conventional_deadlift` | `ex-conventional-deadlift.svg` | 2,822 | Tier 1 (مركب) | بار أولمبي عند منتصف الساق، سحب ميت كلاسيكي مع استقامة الظهر |
| 3 | `incline_barbell_bench_press` | `ex-incline-barbell-bench-press.svg` | 3,116 | Tier 1 (مركب) | بنش مائل عالي 35-40°، ضغط بار عمودي على الصدر العلوي |
| 4 | `incline_dumbbell_press` | `ex-incline-dumbbell-press.svg` | 3,084 | Tier 1 (مركب) | بنش مائل عالي، ضغط زوج دمبل مع تقارب في الأعلى |
| 5 | `dumbbell_bench_press` | `ex-dumbbell-bench-press.svg` | 3,125 | Tier 1 (مركب) | بنش مستوي أفقي، ضغط زوج دمبل متوازي |
| 6 | `seated_cable_row` | `ex-seated-cable-row.svg` | 2,772 | Tier 1 (مركب) | ماكينة كابل أرضي، سحب مقبض V لجدار البطن السفلي |
| 7 | `leg_press` | `ex-leg-press.svg` | 3,017 | Tier 1 (مركب) | مكبس أرجل بزاوية 45°، عربة وأقواس وزن ودفع من الكعبين |
| 8 | `seated_dumbbell_shoulder_press` | `ex-seated-dumbbell-shoulder-press.svg` | 3,197 | Tier 1 (مركب) | مقعد بمسند 90°، ضغط دمبل علوي فردي/زوجي للأكتاف |
| 9 | `hanging_leg_raise` | `ex-hanging-leg-raise.svg` | 2,335 | Tier 1 (مركب) | تعليق على عقلة، رفع الرجلين بزاوية 90° أفقية للبطن |
| 10 | `standing_dumbbell_lateral_raise` | `ex-standing-dumbbell-lateral-raise.svg` | 3,037 | Tier 2 (عزل) | وقوف رياضي، رفع دمبل جانبي لمستوى الكتف (أجنحة) |
| 11 | `barbell_curl` | `ex-barbell-curl.svg` | 2,502 | Tier 2 (عزل) | وقوف، كيرل بايسبس بالبار مستقيم مع ثبات الكوعين |
| 12 | `hammer_curl` | `ex-hammer-curl.svg` | 2,349 | Tier 2 (عزل) | وقوف، قبضة شاكوش محايدة (الإبهام لأعلى) لعضلة البراكيلس |
| 13 | `triceps_rope_pushdown` | `ex-triceps-rope-pushdown.svg` | 2,644 | Tier 2 (عزل) | كابل عالي، دفع الحبل لأسفل مع تباعد طرفي الحبل |
| 14 | `skull_crushers` | `ex-skull-crushers.svg` | 2,606 | Tier 2 (عزل) | استلقاء على بنش، بار EZ يمتد من الجبهة للأعلى عموديًا |
| 15 | `dumbbell_chest_flyes` | `ex-dumbbell-chest-flyes.svg` | 2,577 | Tier 2 (عزل) | استلقاء على بنش، تفتيح الصدر بقوس دائري واسع |
| 16 | `lying_leg_curl_machine` | `ex-lying-leg-curl-machine.svg` | 2,757 | Tier 2 (عزل) | استلقاء على البطن (وجه لأسفل)، ثني الساقين للوراء بالماكينة |
| 17 | `seated_leg_curl_machine` | `ex-seated-leg-curl-machine.svg` | 2,693 | Tier 2 (عزل) | جلوس بالماكينة وتثبيت الفخذين، ثني الساقين لأسفل وأسفل المقعد |
| 18 | `standing_calf_raise_machine` | `ex-standing-calf-raise-machine.svg` | 2,493 | Tier 2 (عزل) | وقوف تحت وسائد الكتف، رفع الكعبين لأعلى على حافة منصة |
| 19 | `seated_palms_up_wrist_curl` | `ex-seated-palms-up-wrist-curl.svg` | 2,970 | Tier 2 (عزل) | جلوس ووضع الساعدين على الفخذين، ثني الرسغ بالبار كف لأعلى |

---

## 2. جدول التغطية الشاملة لتمارين القوالب الجاهزة الـ 26 (100% Covered)

تضم قوالب الجيم الأربعة (`full_body`, `ppl`, `upper_lower`, `bro_split`) بالضبط **26 تمرين كتالوج فريد** تتكرر عبر 59 فتحة تمرين.
يوثّق الجدول التالي تحقيق **نسبة تغطية 100% لجميع هذه التمارين**:

| # | معرّف التمرين (Catalog ID) | الاسم بالعربية | ملف الرسم المرتبط | مصدر الأصل | وجود الملف | مسار العرض في الواجهة | نتيجة التحقق |
|:---:|---|---|---|:---:|:---:|:---:|:---:|
| 1 | `barbell_back_squat` | سكوات خلفي بالبار | `ex-barbell-back-squat.svg` | **جديد (12.1B)** | ✓ (3,333 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 2 | `barbell_bench_press` | بنش برس بالبار مستوي | `ex-a02-bench-press.svg` | قديم (Legacy) | ✓ (2,778 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 3 | `barbell_bent_over_row` | تجديف بالبار مائل | `ex-b02-barbell-row.svg` | قديم (Legacy) | ✓ (2,353 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 4 | `barbell_curl` | كيرل بايسبس بالبار | `ex-barbell-curl.svg` | **جديد (12.1B)** | ✓ (2,502 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 5 | `conventional_deadlift` | الرفعة الميتة كلاسيكي | `ex-conventional-deadlift.svg` | **جديد (12.1B)** | ✓ (2,822 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 6 | `dumbbell_bench_press` | بنش برس بالدمبل مستوي | `ex-dumbbell-bench-press.svg` | **جديد (12.1B)** | ✓ (3,125 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 7 | `dumbbell_chest_flyes` | تجميع دمبل مستوي | `ex-dumbbell-chest-flyes.svg` | **جديد (12.1B)** | ✓ (2,577 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 8 | `face_pull_cable` | فيس بول بالحبل كابل | `ex-a06-face-pull.svg` | قديم (Legacy) | ✓ (2,724 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 9 | `hammer_curl` | كيرل شاكوش بالدمبل | `ex-hammer-curl.svg` | **جديد (12.1B)** | ✓ (2,349 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 10 | `hanging_leg_raise` | رفع الأرجل تعليقاً | `ex-hanging-leg-raise.svg` | **جديد (12.1B)** | ✓ (2,335 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 11 | `incline_barbell_bench_press` | بنش مائل عالي بالبار | `ex-incline-barbell-bench-press.svg` | **جديد (12.1B)** | ✓ (3,116 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 12 | `incline_dumbbell_press` | بنش مائل عالي بالدمبل | `ex-incline-dumbbell-press.svg` | **جديد (12.1B)** | ✓ (3,084 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 13 | `lat_pulldown_wide_grip` | سحب عالي بالماكينة | `ex-a03-lat-pulldown.svg` | قديم (Legacy) | ✓ (2,942 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 14 | `leg_press` | مكبس الأرجل 45 درجة | `ex-leg-press.svg` | **جديد (12.1B)** | ✓ (3,017 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 15 | `lying_leg_curl_machine` | ثني أرجل نائم ماكينة | `ex-lying-leg-curl-machine.svg` | **جديد (12.1B)** | ✓ (2,757 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 16 | `plank` | بلانك ثابت على الأرض | `ex-a05-plank.svg` | قديم (Legacy) | ✓ (2,026 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 17 | `romanian_deadlift_barbell` | ديدليفت روماني بالبار | `ex-b01-romanian-deadlift.svg` | قديم (Legacy) | ✓ (2,386 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 18 | `seated_cable_row` | تجديف كابل جالس | `ex-seated-cable-row.svg` | **جديد (12.1B)** | ✓ (2,772 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 19 | `seated_dumbbell_shoulder_press` | شولدر برس دمبل جالس | `ex-seated-dumbbell-shoulder-press.svg` | **جديد (12.1B)** | ✓ (3,197 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 20 | `seated_leg_curl_machine` | ثني أرجل جالس ماكينة | `ex-seated-leg-curl-machine.svg` | **جديد (12.1B)** | ✓ (2,693 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 21 | `seated_palms_up_wrist_curl` | ثني رسغ كف لأعلى | `ex-seated-palms-up-wrist-curl.svg` | **جديد (12.1B)** | ✓ (2,970 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 22 | `skull_crushers` | سكل كراشر بار EZ | `ex-skull-crushers.svg` | **جديد (12.1B)** | ✓ (2,606 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 23 | `standing_calf_raise_machine` | رفع سمانة واقف ماكينة | `ex-standing-calf-raise-machine.svg` | **جديد (12.1B)** | ✓ (2,493 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 24 | `standing_dumbbell_lateral_raise` | رفرفة كتف جانبي دمبل | `ex-standing-dumbbell-lateral-raise.svg` | **جديد (12.1B)** | ✓ (3,037 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 25 | `standing_overhead_barbell_press` | ضغط أوفرهيد بالبار | `ex-a04-overhead-press.svg` | قديم (Legacy) | ✓ (2,867 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |
| 26 | `triceps_rope_pushdown` | دفع ترايسبس بالحبل | `ex-triceps-rope-pushdown.svg` | **جديد (12.1B)** | ✓ (2,644 B) | `cat.images[0]` ➔ `ex.img` | **PASSED (100%)** |

> بالإضافة إلى ذلك، تم ربط **4 تمارين كلاسيكية أخرى خارج القوالب** بأصولها القديمة المطابقة:
> - `goblet_squat` ➔ `ex-a01-goblet-squat.svg`
> - `push_up` ➔ `ex-b03-push-up.svg`
> - `pull_up` ➔ `ex-b04-pull-up.svg`
> - `walking_lunges_dumbbell` ➔ `ex-b06-lunges.svg`
> وبذلك يرتفع إجمالي التمارين المغطاة بالكامل في `exercise-catalog.js` إلى **30 تمرينًا**.

---

## 3. تكامل العرض في واجهة المستخدم (UI Integration)

تم فحص وتحسين مسارات العرض الحالية دون أي مساس بهيكل الواجهة أو بيانات المستخدم:

1. **بطاقات تمارين الروتين والجلسات (`renderExercises`):**
   - دالة `transformTemplateExerciseToRuntime(ex, ...)` تقرأ `cat.images[0]` وتمرره تلقائيًا كـ `img`.
   - عند عرض بطاقة التمرين، يتحقق النظام من أسبقية الصورة المخصصة للمستخدم:
     ```javascript
     if(imgRecord && imgRecord.type === 'url' && imgRecord.url){
       displayImgSrc = imgRecord.url;
     } else if(imgRecord && imgRecord.type === 'local' && imgRecord.mediaId){
       displayImgSrc = activeExerciseBlobUrls.get(imgRecord.mediaId);
     } else if(ex.img){
       displayImgSrc = ex.img; // الرسم الافتراضي للكتالوج
     }
     ```
   - إذا لم يرفع المستخدم صورة مخصصة، يُعرض الرسم الافتراضي المحلي بدقة ووضوح. وإذا رفع المستخدم صورة مخصصة، تطغى فورًا على الرسم الافتراضي، محققة أسبقية صور المستخدم بنسبة 100%.

2. **موسوعة التمارين الرياضية (`renderEncyclopediaDetailHtml`):**
   - تمت إضافة دعم عرض الرسم التوضيحي داخل بطاقة تفاصيل التمرين في الموسوعة (`encImgSrc`).
   - عند الضغط على أي تمرين مغطى، يظهر الرسم المتجهي بوضوح داخل إطار أنيق أعلى خطوات الأداء.
   - عند إضافة التمرين للروتين عبر زر `➕ إضافة للروتين`، يتم تمرير مسار الرسم تلقائيًا (`img: selectedEx.images[0]`) ليرث التمرين المضاف حديثًا صورته تلقائيًا.

---

## 4. تحديث Service Worker والكاش (v24)

تم تحديث كاش الخدمة وفق قواعد المشروع الصارمة للعمل دون إنترنت:
- **إصدار الكاش الجديد:** `v24` (`const CACHE_VERSION = 'v24';`).
- **إجمالي الأصول المخزنة مسبقًا (`SHELL_ASSETS`):** ارتفع من 76 إلى **95 أصلًا محليًا**.
- **الأصول المضافة حديثًا:** جميع ملفات الـ SVG الـ 19 الجديدة أُدرجت بمساراتها النسبية `./assets/images/exercises/ex-*.svg`.
- تم التحقق من وجود جميع ملفات `SHELL_ASSETS` الـ 95 على القرص بدون أي ملف مفقود.

---

## 5. نتائج بوابة الاختبارات الموحدة (Unified Master Regression Gate)

تم تشغيل البوابة المركزية `scratch/test_master_regression_gate.py` بعد إضافة جناح `Phase 12.1B` الجديد (الجناح العاشر).
جاءت النتائج بتوافق ونجاح بنسبة 100%:

| الجناح (Suite) | المعرّف (ID) | الحالة | الفحوصات الناجحة | المدة الزمنية | الوصف ومجال الفحص |
|:---:|---|:---:|:---:|:---:|---|
| 1 | `phase5b1_1` | **PASS** | 92 / 92 | 4.97s | سياسة الصور، خلو المصدر من صور إناث أو روابط خارجية، وتخزين كاش v21+. |
| 2 | `phase5b1_2` | **PASS** | 94 / 94 | 9.19s | رسومات الروتين A/B، أسبقية صور المستخدم في IndexedDB، واختبار headless browser. |
| 3 | `phase6c` | **PASS** | 36 / 36 | 7.98s | تحليلات التمرين الحجمية، الأرقام القياسية (PRs)، ورسم SVG البياني. |
| 4 | `phase8b` | **PASS** | 37 / 37 | 8.11s | توجيه الإشعارات عبر Service Worker وفحص سلامة الروابط. |
| 5 | `phase9b_notes` | **PASS** | 51 / 51 | 9.60s | محرك الملاحظات الموحد، الفرز والبحث والفلترة ومرفقات الملاحظات. |
| 6 | `phase9b1_2_gate` | **PASS** | 31 / 31 | 7.26s | بوابة قبول الملاحظات الموحدة وخلو العمليات من الآثار الجانبية. |
| 7 | `phase9c1` | **PASS** | 46 / 46 | 0.41s | موسوعة الاستطالات (34 حركة و34 رسم SVG) وتكامل الواجهة. |
| 8 | `phase9c2` | **PASS** | 54 / 54 | 12.30s | مسار الإحماء التفاعلي، استهداف عضلات الروتين، وحفظ الحالة. |
| 9 | `phase9c3` | **PASS** | 56 / 56 | 13.74s | مسار التهدئة التفاعلي بعد التمرين، قفل الروتين، ومطابقة الجلسة. |
| 10 | `phase12_1b` | **PASS** | 43 / 43 | 0.19s | **رسومات الكتالوج الـ 19 الجديدة، تغطية القوالب 100%، وتحديث كاش v24.** |
| **الإجمالي** | **10 أجنحة** | **PASS ✅** | **540 / 540 (100%)** | **73.77s** | **اجتياز كامل وشامل بدون أي فشل أو استثناء.** |

---

## 6. الملفات المعدلة وأسباب التعديل

1. `assets/images/exercises/ex-*.svg` (19 ملفًا جديدًا):
   - إنشاء 19 رسم SVG أصلي لمكافئات تمارين القوالب الجاهزة.
2. `assets/data/exercise-catalog.js`:
   - تعيين مسارات الصور المحلية داخل مصفوفة `images` لـ 30 تمرينًا (19 جديدة + 11 سابقة).
3. `sw.js`:
   - ترقية `CACHE_VERSION` إلى `v24` وإضافة مسارات الـ 19 رسمًا جديدًا إلى `SHELL_ASSETS`.
4. `index.html`:
   - تعديل دالة `renderEncyclopediaDetailHtml` لعرض صورة التمرين في بطاقة تفاصيل الموسوعة.
   - تعديل معالج `encConfirmAddBtn` لتمرير مسار صورة الكتالوج عند إضافة تمرين للروتين.
5. `zatoona.html`:
   - مزامنة كاملة وتطابق ثنائي بايت لبايت مع `index.html`.
6. `scratch/test_phase12_1b_exercise_images.py`:
   - إنشاء جناح اختبار الانحدار المستقل للتحقق من الرسوم والكاش والتغطية (43 فحصًا).
7. `scratch/test_master_regression_gate.py`:
   - تسجيل الجناح العاشر `phase12_1b` ضمن قائمة الأجنحة النشطة للبوابة المركزية.

---

## 7. بوابة الإغلاق النهائية وسلامة البيئة

- **التطابق الثنائي لملفات HTML:**
  - الأمر: `fc.exe /b index.html zatoona.html`
  - النتيجة: **`FC: no differences encountered` (100% تطابق تام)**.
- **بصمات SHA-256 للملفات الأساسية بعد التعديل:**
  - `index.html`: `10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957` (1,221,201 بايت)
  - `zatoona.html`: `10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957` (1,221,201 بايت)
  - `sw.js`: `7AB40099A5529823119CD5FB1A85AF88FAB26546FE2B8885D974B792063130C3` (20,545 بايت)
  - `assets/data/exercise-catalog.js`: `BC6320D1CA83A748F3F15722010388CDA2333FC7AEE3C267840AB6C42EDAAC26` (139,227 بايت)
  - `manifest.json`: `C872752E51F5B339BD3965370B5DF54B47CBAAAD398785F85D6453FD93C743E5` (1,022 بايت — لم يتغير)
- **فحص المسافات ونهايات الأسطر:** `git diff --check` انتهى دون أي أخطاء (Code 0).
- **التخزين وبيانات المستخدم:** لم يتم فتح أو مسح أو تعديل أي بيانات في LocalStorage أو IndexedDB.
- **الالتزام بالقواعد الإلزامية:** لم يتم تنفيذ `git commit` أو `push` أو `deploy`.
- **التوقف الإلزامي:** تم التوقف التام فور اكتمال متطلبات Phase 12.1B بنجاح.
