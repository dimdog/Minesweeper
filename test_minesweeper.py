from unittest import TestCase
from minesweeper import MineSweeper


class TestMineSweeper(TestCase):

    def test_add_mine(self):
        ms = MineSweeper(3, 3, 0)
        ms.add_mine(0, 0)
        # M 1 0
        # 1 0 0
        # 0 0 0
        self.assertEqual(ms.grid[0][0].value, -1)
        self.assertEqual(ms.grid[0][1].value, 1)
        self.assertEqual(ms.grid[1][0].value, 1)
        ms.add_mine(1, 1)
        # M 2 1
        # 2 M 1
        # 1 1 1
        self.assertEqual(ms.grid[0][0].value, -1)
        self.assertEqual(ms.grid[1][1].value, -1)
        self.assertEqual(ms.grid[0][1].value, 2)
        self.assertEqual(ms.grid[1][0].value, 2)
        self.assertEqual(ms.grid[0][2].value, 1)
        self.assertEqual(ms.grid[2][0].value, 1)
        self.assertEqual(ms.grid[1][2].value, 1)
        self.assertEqual(ms.grid[2][1].value, 1)
        self.assertEqual(ms.grid[2][2].value, 1)
