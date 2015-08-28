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

    # 1 merge down
    def test_legal_move1(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 0, 0, 0], [4, 8, 0, 0], [2, 4, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.DOWN), 1)

    # 1 merge down
    def test_legal_move2(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 0, 0, 0], [8, 8, 0, 0], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.DOWN), 1)

    # 1 merge up
    def test_legal_move3(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 2, 4], [4, 0, 4, 2], [8, 8, 2, 8], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.UP), 1)

    # 1 merge up
    def test_legal_move4(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 0, 0, 0], [4, 4, 0, 0], [2, 4, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.LEFT), 1)

    # 2 merges down
    def test_legal_move5(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 8, 0, 0], [4, 8, 0, 0], [2, 4, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.DOWN), 2)

    # 2 merges down
    def test_legal_move6(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 0, 0, 0], [8, 8, 0, 4], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.DOWN), 2)

    # 2 merges up
    def test_legal_move7(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 4, 2, 4], [2, 0, 0, 0], [8, 8, 0, 4], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.RIGHT), 2)

    # 2 merges left
    def test_legal_move8(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 2, 0, 0], [4, 4, 0, 0], [4, 8, 0, 0], [2, 4, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.LEFT), 2)

    def test_illegal_move1(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 0, 0, 0], [4, 0, 0, 0], [4, 8, 0, 0], [2, 4, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.LEFT), 0)

    def test_illegal_move2(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[0, 0, 0, 2], [0, 0, 0, 4], [0, 0, 0, 8], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.RIGHT), 0)

    def test_illegal_move3(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[0, 0, 0, 0], [0, 0, 0, 0], [4, 2, 8, 2], [2, 8, 16, 4]])
        print game
        self.assertEqual(game.check_move(game_2048.DOWN), 0)

    def test_illegal_move4(self):
        game = game_2048.TwentyFortyEight(4, 4)
        game.set_grid([[2, 4, 4, 2], [4, 8, 2, 0], [8, 2, 0, 0], [16, 0, 0, 0]])
        print game
        self.assertEqual(game.check_move(game_2048.UP), 0)

if __name__ == '__main__':
    unittest.main()
