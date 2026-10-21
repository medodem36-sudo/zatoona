import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def find_fn(name):
    idx = text.find('function ' + name)
    if idx == -1:
        idx = text.find(name + ' = function')
    if idx == -1:
        idx = text.find('const ' + name + ' =')
    if idx != -1:
        line_no = text[:idx].count('\n') + 1
        return f'{name} @ line {line_no}'
    return f'{name}: NOT FOUND'

print('=== PHASE 3 & 4: GYM MANAGEMENT, PLANS, TEMPLATES & ENCYCLOPEDIA ===')
target_fns = [
    # Phase 3
    'getAllExerciseDefinitions', 'getRoutineExercises', 'loadExerciseOverrides', 'saveExerciseOverrides',
    'loadExcludedExercises', 'saveExcludedExercises', 'loadGymRoutineOrder', 'saveGymRoutineOrder',
    'renderGymExManager', 'addCustomExercise', 'editExercise', 'excludeExercise', 'restoreExercise',
    # Phase 4C.1 - 4C.3
    'loadGymPlanConfig', 'saveGymPlanConfig', 'resolveGymRoutine', 'getEffectiveGymDay',
    # Phase 4C.2 Templates
    'GYM_PLAN_TEMPLATE_REGISTRY', 'READY_TEMPLATES', 'applyTemplatePlan',
    # Phase 4C.5 - 4C.7 Custom Plans
    'loadCustomPlans', 'saveCustomPlans', 'createCustomPlan', 'duplicateCustomPlan', 'deleteCustomPlan',
    'setActiveCustomPlan', 'renderCustomPlanEditor',
    # Phase 3B Encyclopedia
    'renderGymEncyclopedia', 'searchEncyclopedia', 'filterEncyclopedia',
    # Overrides & Settings
    'loadGymDayOverrides', 'saveGymDayOverrides', 'isGymEnabled', 'isGymPaused',
    'loadGymWeeklySchedule', 'saveGymWeeklySchedule'
]

for fn in target_fns:
    print(' ', find_fn(fn))

# Check exercise-catalog.js size and import
print('\n=== EXERCISE CATALOG FILE AUDIT ===')
cat_path = os.path.join('assets', 'data', 'exercise-catalog.js')
if os.path.exists(cat_path):
    sz = os.path.getsize(cat_path)
    with open(cat_path, 'r', encoding='utf-8') as cf:
        cat_text = cf.read()
    ex_count = len(re.findall(r'id:\s*["\']', cat_text))
    print(f'Catalog file exists: {cat_path} ({sz:,} bytes), exercises count: {ex_count}')
else:
    print('Catalog file NOT FOUND at assets/data/exercise-catalog.js!')
