# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.controllers.action_controller import ActionController
from game.common.enums import *
from game.common.TrUpgrades.BodyObjects.sentry_gun import SentryGun


# Your test class is a subclass of unittest.Testcase, this is important
class TestUpgradesentryGun(unittest.TestCase):

    # This method is used to set up anything you wish to test prior to every test method below.
    def setUp(self):
        self.myPlayer = Player(12, "Sean")
        self.myPlayer.truck.money = 10000
        self.actionCont = ActionController()

    # Test methods should always start with the word 'test'
    def test_valid_speed(self):
        sped = stats.GameStats.truck_maximum_speed
        self.myPlayer.truck.set_current_speed(sped)
        self.assertEqual(sped,self.myPlayer.truck.get_current_speed())

    def test_bad_speed(self):
        sped = stats.GameStats.truck_maximum_speed + 1
        self.myPlayer.truck.set_current_speed(sped)
        self.assertEqual(stats.GameStats.truck_maximum_speed ,self.myPlayer.truck.get_current_speed())

    def test_negative_speed(self):
        sped = 0
        self.myPlayer.truck.set_current_speed(sped)
        self.assertEqual(1,self.myPlayer.truck.get_current_speed())

    def test_illegal_set(self):
        sped = stats.GameStats.truck_maximum_speed + 1
        self.myPlayer.truck.__speed = sped
        self.assertNotEqual(sped ,self.myPlayer.truck.get_current_speed())

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
