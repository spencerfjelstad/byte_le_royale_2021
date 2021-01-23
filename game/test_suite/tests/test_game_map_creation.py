import unittest

from game.utils.create_game_map import create_game_map
from game.common.game_map import Game_Map
from game.common.node import Node
from game.common.road import Road

class TestGameMapCreation(unittest.TestCase):

    def setUp(self):
        self.test_map = create_game_map(3, 300)
    
    def test_map_length(self):
        self.assertEqual(self.test_map.length(), 4)
        for i in range(self.test_map.length() - 1):
            curr = self.test_map.head
            for j in curr.roads:
               self.assertTrue(80 <= j.length <= 120)

    # def test_map_names(self):
    #     self.assertEqual(self.test_map.current_node.city_name, "1")
    #     last = None
    #     temp = True
    #     while temp != False:
    #         temp = self.test_map.get_next_node()
    #         if temp != False:
    #             last = temp
    #     self.assertEqual(last.city_name, "end")

if __name__ == '__main__':
    unittest.main
