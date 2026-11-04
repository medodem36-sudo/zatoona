import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('scratch'))

import unittest
from test_phase3_gym_engine import TestPhase3GymEngine

suite = unittest.TestSuite()
suite.addTest(TestPhase3GymEngine('test_04_gym_tools_quick_bar_rendered_in_gym_mode'))
suite.addTest(TestPhase3GymEngine('test_10_gym_big_numbers_focus_mode'))
suite.addTest(TestPhase3GymEngine('test_12_injury_and_pain_flagging'))
suite.addTest(TestPhase3GymEngine('test_13_exercise_card_actions_row'))
suite.addTest(TestPhase3GymEngine('test_14_ongoing_workout_hud_presence'))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
print("Was successful:", result.wasSuccessful())
