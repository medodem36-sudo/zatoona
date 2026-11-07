# Test and preview the expanded EGYPTIAN_POPULAR_FOODS and Weekly Meal Plan

egyptian_foods_sample = [
    {
        'id': 'sardines_alex_med',
        'name': 'سردين بلدي إسكندراني (طازج من البحر المتوسط)',
        'portion': 'حصة 150 جم مشوي بالردة والليمون',
        'kcal': 250, 'p': 32, 'c': 0, 'f': 13.5, 'icon': '🐟', 'category': 'protein',
        'tip': 'صيد بحري طازج من شواطئ الإسكندرية. منجم طبيعي لأوميجا 3 (EPA/DHA)، كالسيوم العظام الطبيعي، فيتامين D، والسيلينيوم وفيتامين B12. مثالي للبناء العضلي وصحة القلب.'
    },
    {
        'id': 'bolti_grilled',
        'name': 'سمك بلطي نيلي مشوي بالردة',
        'portion': 'سمكة وسط 250 جم صافي',
        'kcal': 230, 'p': 44, 'c': 0, 'f': 5.5, 'icon': '🐟', 'category': 'protein',
        'tip': 'أشهر سمك مصري وأعلى قيمة بروتين نقي بأقل نسبة دهون، خفيف وسهل الهضم.'
    }
]

print("Expanded foods test ok, items:", len(egyptian_foods_sample))
