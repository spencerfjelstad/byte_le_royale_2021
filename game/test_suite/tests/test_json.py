# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.
from game.common import stats
from game.utils import helpers
import unittest
from game.common.player import Player
from game.controllers.action_controller import ActionController
from game.common.enums import *
from game.common.TrUpgrades.gps import GPS
import copy


# Your test class is a subclass of unittest.Testcase, this is important
class TestJSON(unittest.TestCase):

    # This method is used to set up anything you wish to test prior to every test method below.
    def setUp(self):
        self.myPlayer = Player(12, "Sean")
        self.myPlayer.truck.money = 10000
        self.actionCont = ActionController()

    # Test methods should always start with the word 'test'
    def test_to_and_back(self):
        breakpoint()
        bruh = copy.deepcopy(self.myPlayer.truck)
        tojsn = self.myPlayer.truck.to_json()
        trk = Player(2131, 'John')
        trk.truck.from_json(tojsn)
        self.assertEqual(bruh.to_json(), trk.truck.to_json())


 

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
