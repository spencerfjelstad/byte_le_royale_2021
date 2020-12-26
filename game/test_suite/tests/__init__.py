# When you create a new test file, make sure to add it here.
# Simply import the class from your file, and then add that class to the '__all__' array.

from game.test_suite.tests.test_example import TestExample
from game.test_suite.tests.test_game_map_creation import TestGameMapCreation

__all__ = [
    'TestExample',
    'TestGameMapCreation'
]