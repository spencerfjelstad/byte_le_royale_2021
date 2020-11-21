# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.controllers.action_controller import ActionController
from game.common.enums import *


class TestUpgradeTank(unittest.TestCase): # Your test class is a subclass of unittest.Testcase, this is important

    def setUp(self): # This method is used to set up anything you wish to test prior to every test method below.
        self.myPlayer = Player(12,"Sean")
        self.myPlayer.money = 10000
        self.actionCont = ActionController()
    
    def test_upgrade_one_level(self): # Test methods should always start with the word 'test'
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 10000
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_one)
    
    def test_upgrade_two_level(self):
        self.myPlayer.truck.body.level = 0
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_two)

    def test_upgrade_beyond_allowable(self):
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 100000
        expectedCash = self.myPlayer.money - helpers.addTogetherDictValues(stats.GameStats.gas_upgrade_cost)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_three)
        self.assertEqual(self.myPlayer.money, expectedCash)

    def test_no_money(self):
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 10
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_zero)
        self.assertEqual(self.myPlayer.money, 10)


    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
