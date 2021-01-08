# When you create a new test file, make sure to add it here.
# Simply import the class from your file, and then add that class to the '__all__' array.

from game.test_suite.tests.test_upgrade_scanner import TestUpgradeScanner
from game.test_suite.tests.test_upgrade_tires import TestUpgradeTires
from game.test_suite.tests.test_upgrade_tank import TestUpgradeTank
from game.test_suite.tests.test_upgrade_headlights import TestUpgradeHeadlights
from game.test_suite.tests.test_upgrade_gun import TestUpgradesentryGun
from game.test_suite.tests.test_upgrade_rabbit_foot import TestUpgradeRabbitFoot
from game.test_suite.tests.test_upgrade_gps import TestUpgradeGPS
from game.test_suite.tests.test_example import TestExample
from game.test_suite.tests.test_game_map_creation import TestGameMapCreation
from game.test_suite.tests.test_json import TestJSON
from game.test_suite.tests.test_action_controller import TestActionController




__all__ = [
    'TestUpgradeScanner',
    'TestUpgradeTires',
    'TestUpgradeTank', 
    'TestUpgradeHeadlights',
    'TestUpgradesentryGun',
    'TestUpgradeRabbitFoot',
    'TestUpgradeGPS',
    'TestGameMapCreation',
    'TestActionController'
    #'TestJSON'
]
