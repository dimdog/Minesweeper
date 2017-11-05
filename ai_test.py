from unittest import TestCase
from minesweeper import MineSweeper
from ai import MinesweeperAI


class TestMinesweeperAI(TestCase):

    def setUp(self):
        self.ms = None

    def count_marked_cells(self):
        count = 0
        for row in self.ms.grid:
            for cell in row:
                count += 1 if cell.marked else 0
        return count

    def test_pick_cell_basic(self):
        self.ms = MineSweeper(4, 4, 0)
        ai = MinesweeperAI(self.ms)
#        ----------------------------------------
#        0| ?, ?, 1, 0,
#        1| ?, ?, 2, 1,
#        2| ?, ?, ?, ?,
#        3| ?, ?, ?, ?,
#        ----------------------------------------
        self.ms.add_mine(0, 1)
        self.ms.add_mine(2, 3)
        self.ms.pick_cell(0, 3)
        self.ms.display_grid()
        cell = ai.reveal_cell()
        self.assertEquals(cell, (2, 1))

    def test_mark_cells_basic_one(self):
        self.ms = MineSweeper(3, 3, 0)
        ai = MinesweeperAI(self.ms)
        self.ms.add_mine(0, 0)
        for y in xrange(len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                if y != 0 and x != 0:
                    self.ms.pick_cell(y, x)
        # B 1 0
        # 1 1 0
        # 0 0 0
        ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 1)
        self.assertEqual(self.ms.grid[0][0].marked, True)

    def test_mark_cells_basic_three(self):
        self.ms = MineSweeper(3, 3, 0)
        ai = MinesweeperAI(self.ms)
        self.ms.add_mine(0, 0)
        self.ms.add_mine(0, 1)
        self.ms.add_mine(0, 2)
        for y in xrange(1, len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                self.ms.pick_cell(y, x)
        # B B B
        # 2 3 2
        # 0 0 0
        ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 3)
        self.assertEqual(self.ms.grid[0][0].marked, True)
        self.assertEqual(self.ms.grid[0][1].marked, True)
        self.assertEqual(self.ms.grid[0][2].marked, True)

    def test_mark_cells_adjacents(self):
        self.ms = MineSweeper(3, 3, 0)
        ai = MinesweeperAI(self.ms)
        self.ms.add_mine(0, 0)
        self.ms.pick_cell(0, 1)
        self.ms.pick_cell(1, 0)
        # Can't mark yet, not enough info! (could be 0,0 or 1,1)
        # B 1 ?
        # 1 ? ?
        # ? ? ?
        ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 0)
        self.ms.add_mine(1, 1)
        # B 2 ?
        # 2 B ?
        # ? ? ?
        ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 0)
        # Reveal top right, Adjacency should give us top left
        # B 2 1
        # 2 B ?
        # ? ? ?
        self.ms.pick_cell(0, 2)
        ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 1)
        self.assertEqual(self.ms.grid[0][0].marked, True)

    def test_mark_cells_adjacents_two(self):
        # B ? B
        # 1 2 1
        # 0 0 0
        self.ms = MineSweeper(3, 3, 0)
        ai = MinesweeperAI(self.ms)
        self.ms.add_mine(0, 0)
        self.ms.add_mine(0, 2)
        for y in xrange(1, len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                self.ms.pick_cell(y, x)
        ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 2)
        self.assertEqual(self.ms.grid[0][0].marked, True)
        self.assertEqual(self.ms.grid[0][2].marked, True)
