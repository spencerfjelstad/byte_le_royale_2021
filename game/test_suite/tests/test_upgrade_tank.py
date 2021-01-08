# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.
<<<<<<< HEAD
from game.common.TrUpgrades.police_scanner import PoliceScanner
=======
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.controllers.action_controller import ActionController
from game.common.enums import *
from game.common.TrUpgrades.BodyObjects.tank import Tank
from game.common.TrUpgrades.BodyObjects.headlights import HeadLights


# Your test class is a subclass of unittest.Testcase, this is important
class TestUpgradeTank(unittest.TestCase):

    # This method is used to set up anything you wish to test prior to every test method below.
    def setUp(self):
        self.myPlayer = Player(12, "Sean")
        self.myPlayer.money = 10000
        self.actionCont = ActionController()

    # Test methods should always start with the word 'test'
    def test_upgrade_one_level(self):
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 10000
<<<<<<< HEAD
        expectedCash = 10000 - stats.GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][1]
=======
        expectedCash = 10000 - stats.GameStats.tank_upgrade_cost[1]
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_one)
        self.assertEqual(expectedCash, self.myPlayer.money)
        self.assertTrue(isinstance(self.myPlayer.truck.body, Tank))

    def test_upgrade_two_level(self):
        self.myPlayer.truck.body.level = 0
<<<<<<< HEAD
        expectedCash = 10000 -  stats.GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][1] -  stats.GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][2]
=======
        expectedCash = 10000 - stats.GameStats.tank_upgrade_cost[1] - stats.GameStats.tank_upgrade_cost[2]
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_two)
        self.assertEqual(expectedCash, self.myPlayer.money)
        self.assertTrue(isinstance(self.myPlayer.truck.body, Tank))

    def test_upgrade_beyond_allowable(self):
<<<<<<< HEAD
        self.myPlayer.truck.body = PoliceScanner()
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 100000
        expectedCash = self.myPlayer.money - \
            helpers.addTogetherDictValues( stats.GameStats.costs_and_effectiveness[ObjectType.tank]['cost'])
=======
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 100000
        expectedCash = self.myPlayer.money - \
            helpers.addTogetherDictValues(stats.GameStats.tank_upgrade_cost)
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_three)
        self.assertEqual(self.myPlayer.money, expectedCash)
        self.assertTrue(isinstance(self.myPlayer.truck.body, Tank))

    def test_no_money(self):
        self.myPlayer.truck.body.level = 0
        self.myPlayer.money = 1
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.tank)
        self.assertEqual(self.myPlayer.truck.body.level, TankLevel.level_zero)
        self.assertEqual(self.myPlayer.money, 1)

    def test_not_tank(self):
        self.myPlayer.truck.body = HeadLights()
        self.myPlayer.money = 1
<<<<<<< HEAD
        self.assertEqual(self.myPlayer.truck.body.current_gas,  stats.GameStats.costs_and_effectiveness[ObjectType.tank]['effectiveness'][0] * stats.GameStats.truck_starting_gas)
        self.assertEqual(self.myPlayer.truck.body.max_gas, stats.GameStats.costs_and_effectiveness[ObjectType.tank]['effectiveness'][0] * stats.GameStats.truck_starting_gas)
=======
        self.assertEqual(self.myPlayer.truck.body.current_gas, stats.GameStats.gas_max_level[TankLevel.level_zero])
        self.assertEqual(self.myPlayer.truck.body.max_gas, stats.GameStats.gas_max_level[TankLevel.level_zero])
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
        self.assertEqual(self.myPlayer.money, 1)

    def test_not_tank_upgrade(self):
        self.myPlayer.truck.body = HeadLights()
        self.myPlayer.money = 10000
<<<<<<< HEAD
        expectedCash = 10000 -  stats.GameStats.costs_and_effectiveness[ObjectType.headlights]['cost'][1]
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.headlights)
        self.assertEqual(self.myPlayer.truck.body.level, HeadlightLevel.level_one)
        self.assertEqual(self.myPlayer.truck.body.current_gas, stats.GameStats.costs_and_effectiveness[ObjectType.tank]['effectiveness'][0] * stats.GameStats.truck_starting_gas)
        self.assertEqual(self.myPlayer.truck.body.max_gas, stats.GameStats.costs_and_effectiveness[ObjectType.tank]['effectiveness'][0] * stats.GameStats.truck_starting_gas)
=======
        expectedCash = 10000 - stats.GameStats.headlight_upgrade_cost[1]
        self.actionCont.upgrade_level(self.myPlayer, ObjectType.headlights)
        self.assertEqual(self.myPlayer.truck.body.level, HeadlightLevel.level_one)
        self.assertEqual(self.myPlayer.truck.body.current_gas, stats.GameStats.gas_max_level[TankLevel.level_zero])
        self.assertEqual(self.myPlayer.truck.body.max_gas, stats.GameStats.gas_max_level[TankLevel.level_zero])
>>>>>>> f346ae434ff14b310ac48b62292000359d84b789
        self.assertEqual(self.myPlayer.money, expectedCash)
    

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
