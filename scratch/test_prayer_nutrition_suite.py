# -*- coding: utf-8 -*-
import unittest
import re

class TestPrayerAndNutritionEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('index.html', 'r', encoding='utf-8') as f:
            cls.html = f.read()

    def test_dynamic_status_capsule_html_initially_hidden(self):
        self.assertIn('id="dynamicStatusCapsule"', self.html)
        self.assertIn('style="display:none;"', self.html)
        self.assertIn('id="capsuleLiveContent">🕌 جاري تحديد الصلاة القادمة...</span>', self.html)

    def test_no_hardcoded_asr_in_capsule_or_summary(self):
        # Ensure '🕌 العصر: 03:15 م (قادم)' is NOT in index.html
        self.assertNotIn('🕌 العصر: 03:15 م (قادم)', self.html)
        # Ensure buildAllInOneDailySummary does not hardcode Asr
        m = re.search(r'function buildAllInOneDailySummary\(\)\{[\s\S]*?return\s*\{([\s\S]*?)\};', self.html)
        self.assertTrue(m, "buildAllInOneDailySummary not found")
        body = m.group(1)
        self.assertNotIn("'العصر'", body)
        self.assertNotIn("'03:15 م'", body)

    def test_sardines_in_food_db_defaults(self):
        self.assertIn('sardinesAlex:', self.html)
        self.assertIn('سردين بلدي إسكندراني طازج', self.html)
        self.assertIn('sardinesAlex', self.html)

    def test_expanded_egyptian_food_catalog(self):
        self.assertIn('sardines_alex_med', self.html)
        self.assertIn('سردين بلدي إسكندراني (طازج من البحر المتوسط)', self.html)
        self.assertIn('bolti_grilled', self.html)
        self.assertIn('areesh_cheese_baladi', self.html)
        self.assertIn('boiled_eggs_baladi', self.html)
        self.assertIn('foul_mudammas_zeyt_harr', self.html)
        self.assertIn('dates_baladi_rotab', self.html)

    def test_weekly_meal_plan_elements(self):
        self.assertIn('modalWeeklyMealPlan', self.html)
        self.assertIn('btnOpenWeeklyMealPlan', self.html)
        self.assertIn('chkLimitlessManMax', self.html)
        self.assertIn('limitlessManMaxSynergyBox', self.html)
        self.assertIn('openWeeklyMealPlanModal', self.html)
        self.assertIn('applyWeeklyMealPlanDayToToday', self.html)
        self.assertIn('applyWeeklyMealPlanToEntireWeek', self.html)

    def test_limitless_man_max_synergy_content(self):
        self.assertIn('ليمتليس مان ماكس الزرقاء للرجال', self.html)
        self.assertIn('11 مجم', self.html)
        self.assertIn('1000 IU', self.html)
        self.assertIn('أوميجا 3', self.html)

    def test_weekly_plan_template_structure(self):
        self.assertIn('WEEKLY_PLAN_TEMPLATE', self.html)
        self.assertIn('سردين بلدي إسكندراني طازج من البحر المتوسط (160 جم)', self.html)
        self.assertIn('صدور دجاج مشوية (150 جم مطبوخ)', self.html)
        self.assertIn('كفتة لحم بقري بلدي مشوية خفيفة (160 جم)', self.html)
        self.assertIn('سمك بلطي نيلي مشوي بالردة (200 جم صافي)', self.html)
        self.assertIn('علبة تونة قطع لحم أبيض في ماء (140 جم صافي)', self.html)
        self.assertIn('كبدة بلدي إسكندراني بالثوم والليمون والفلفل (150 جم)', self.html)

if __name__ == '__main__':
    unittest.main()
