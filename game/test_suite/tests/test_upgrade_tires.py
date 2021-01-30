# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

from game.common.stats import GameStats
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.controllers.action_controller import ActionController
from game.common.enums import *


class TestUpgradeTires(unittest.TestCase): # Your test class is a subclass of unittest.Testcase, this is important

    def setUp(self): # This method is used to set up anything you wish to test prior to every test method below.
        self.myPlayer = Player(12,"Sean")
        self.myPlayer.truck.money = 10000
        self.actionCont = ActionController()
    
    def test_upgrade_sticky(self):
        self.myPlayer.truck.tires = TireType.tire_normal
        self.myPlayer.truck.money = 10000
        expectedCash = 10000 - stats.GameStats.tire_switch_cost
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, TireType.tire_sticky)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_sticky)
        self.assertEqual(expectedCash, self.myPlayer.truck.money)

    def test_upgrade_econ(self):
        self.myPlayer.truck.tires = TireType.tire_normal
        self.myPlayer.truck.money = 10000
        expectedCash = 10000 - stats.GameStats.tire_switch_cost
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, TireType.tire_econ)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_econ)

    def test_upgrade_normal(self):
        self.myPlayer.truck.tires = TireType.tire_sticky
        self.myPlayer.truck.money = 10000
        expectedCash = 10000 - stats.GameStats.tire_switch_cost
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, TireType.tire_normal)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_normal)
    
    
    def test_same_type(self):
        self.myPlayer.truck.money = 10000
        expectedCash = 10000
        self.myPlayer.truck.tires = TireType.tire_normal
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, TireType.tire_normal)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_normal)
        self.assertEqual(self.myPlayer.truck.money, expectedCash)

    def test_upgrade_beyond_allowable(self):
        self.myPlayer.truck.tires = TireType.tire_normal
        self.myPlayer.truck.money = 10000
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, 10)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_normal)
        self.assertEqual(self.myPlayer.truck.money, 10000)

    def test_no_money(self):
        self.myPlayer.truck.tires = TireType.tire_normal
        self.myPlayer.truck.money = 10
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tires, TireType.tire_sticky)
        self.assertEqual(self.myPlayer.truck.tires, TireType.tire_normal)
        self.assertEqual(self.myPlayer.truck.money, 10)


    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
