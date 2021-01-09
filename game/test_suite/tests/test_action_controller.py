# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.common.node import Node
from game.common.node import Road
from game.controllers.action_controller import ActionController
from game.common.enums import EventType, RoadType, ObjectType, TireType
from game.common.TrUpgrades.BodyObjects.sentry_gun import SentryGun



# Your test class is a subclass of unittest.Testcase, this is important
class TestActionController(unittest.TestCase):

    # This method is used to set up anything you wish to test prior to every test method below.
    def setUp(self):
        self.myPlayer = Player(12, "Sean")
        self.myPlayer.money = 10000
        self.actionCont = ActionController()

    # Test methods should always start with the word 'test'
    #def test_valid_move(self):
        #breakpoint()
        # self.myPlayer.active_contract_index = 0
        # self.actionCont.select_contract(self.myPlayer)
        # nextNode = self.myPlayer.truck.current_node.next_node
        # startGas = self.myPlayer.truck.body.current_gas
        # self.actionCont.move(self.myPlayer, self.myPlayer.truck.current_node.roads[0])
        # self.assertEqual(nextNode, self.myPlayer.truck.current_node)
        # self.assertGreater(startGas, self.myPlayer.truck.body.current_gas)

    # def test_invalid_move(self):
    #     nextNode = self.myPlayer.truck.current_node.next_node
    #     startGas = self.myPlayer.truck.body.current_gas
    #     rd = Road('TheWrongWay',RoadType.city_road, 10000)
    #     self.actionCont.move(self.myPlayer, rd)
    #     self.assertNotEqual(nextNode, self.myPlayer.truck.current_node)
    #     self.assertEqual(startGas, self.myPlayer.truck.body.current_gas)

    def test_event_controller_tires(self):
        neg = stats.GameStats.costs_and_effectiveness[ObjectType.tires]['effectiveness'][self.myPlayer.truck.tires]
        actneg = self.actionCont.event_controller.negation(self.myPlayer.truck, EventType.icy_road)
        self.assertAlmostEqual(neg, actneg["DamageMod"])
        self.assertAlmostEqual(neg, actneg["HealthMod"])

    def test_event_controller_tires_upgrade(self):
        self.myPlayer.truck.tires = TireType.tire_sticky
        neg = stats.GameStats.costs_and_effectiveness[ObjectType.tires]['effectiveness'][self.myPlayer.truck.tires]
        actneg = self.actionCont.event_controller.negation(self.myPlayer.truck, EventType.icy_road)
        self.assertAlmostEqual(neg, actneg['DamageMod'])
        self.assertAlmostEqual(neg, actneg['HealthMod'])

    def test_event_controller_sentry_gun(self):
        self.myPlayer.truck.body = SentryGun()
        neg = stats.GameStats.costs_and_effectiveness[ObjectType.sentryGun]['effectiveness'][self.myPlayer.truck.body.level]
        actneg = self.actionCont.event_controller.negation(self.myPlayer.truck, EventType.bandits)
        self.assertAlmostEqual(neg, actneg["DamageMod"])
        self.assertAlmostEqual(neg, actneg["HealthMod"])




    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
