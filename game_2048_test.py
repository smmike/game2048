__author__ = 'mismirno'

import unittest
import game_2048


class MyTestCase(unittest.TestCase):
    def test_init_sets_grid_width(self):
        game = game_2048.TwentyFortyEight(3, 5)
        self.assertEqual(game.get_grid_width, 5)

    def test_init_sets_grid_height(self):
        game = game_2048.TwentyFortyEight(3, 5)
        self.assertEqual(game.get_grid_height, 3)

    def test_init_minimal_dimensions(self):
        game = game_2048.TwentyFortyEight(2, 2)
        self.assertEqual(game.get_grid_width, 2)
        self.assertEqual(game.get_grid_width, 2)



if __name__ == '__main__':
    unittest.main()
