from unittest import TestCase
from minesweeper import MineSweeper


class TestMinesweeperAI(TestCase):

    def setUp(self):
        self.ms = None

    def count_marked_cells(self):
        count = 0
        for row in self.ms.grid:
            for cell in row:
                count += 1 if cell.marked else 0
        return count

    def test_reveal_cell_basic(self):
        self.ms = MineSweeper(4, 4, 0)
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
        cell = self.ms.ai.reveal_cell()
        self.assertEquals(cell, (2, 1))

    def test_reveal_cell_complex(self):
        """ Present it a situation where it *must* use adjaceny rules"""
#        ----------------------------------------
#        0| 1, M, B, ?,
#        1| 2, 3, 2, ?,
#        2| 1, M, ?, ?,
#        ----------------------------------------
        self.ms = MineSweeper(3, 4, 0)
        self.ms.add_mine(0, 1)
        self.ms.add_mine(2, 1)
        self.ms.add_mine(0, 2)
        self.ms.pick_cell(0, 0)
        self.ms.pick_cell(1, 0)
        self.ms.pick_cell(2, 0)
        self.ms.pick_cell(1, 1)
        self.ms.pick_cell(1, 2)
        self.ms.mark_cell(0, 1)
        self.ms.mark_cell(0, 2)
        # ----
        pick = self.ms.ai.reveal_cell()
        self.assertIn(pick, {(0, 3), (1, 3), (2, 3)})
        self.assertEqual(self.ms.ai.guessing, False)

    def test_reveal_cell_guess(self):
        """ Present it a situation where it *must* guess"""
#        ----------------------------------------
#        0| 1, M, B, ?,
#        1| 2, 3, 3, ?,
#        2| 1, M, ?, B,
#        ----------------------------------------
        self.ms = MineSweeper(3, 4, 0)
        self.ms.add_mine(0, 1)
        self.ms.add_mine(2, 1)
        self.ms.add_mine(0, 2)
        self.ms.add_mine(2, 3)
        self.ms.pick_cell(0, 0)
        self.ms.pick_cell(1, 0)
        self.ms.pick_cell(2, 0)
        self.ms.pick_cell(1, 1)
        self.ms.pick_cell(1, 2)
        self.ms.mark_cell(0, 1)
        self.ms.mark_cell(0, 2)
        # ----
        pick = self.ms.ai.reveal_cell()
        self.assertIn(pick, {(0, 3), (1, 3), (2, 3)})
        self.assertEqual(self.ms.ai.guessing, True)

    def test_brute_force(self):
        """ loop over a number of grids, making sure we only fail on random guesses"""
        wins = 0
        losses = 0
        games = 1
        for i in xrange(games):
            self.ms = MineSweeper(16, 30, 99)  # standard expert grid
            while not self.ms.victory and not self.ms.game_over:
                self.ms.ai.mark_cells()
                pick = self.ms.ai.reveal_cell()
                self.ms.pick_cell(*pick)
            if self.ms.victory:
                wins += 1
            if self.ms.game_over:
                if self.ms.ai.guessing:
                    losses += 1
                else:
                    self.ms.display_grid()
                    print pick
                    assert 0, "Lost on a non guess"

        print "Games:{}\n\tWins:{}\n\tLosses:{}".format(games, wins, losses)

    def test_mark_cells_basic_one(self):
        self.ms = MineSweeper(3, 3, 0)
        self.ms.add_mine(0, 0)
        for y in xrange(len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                if y != 0 and x != 0:
                    self.ms.pick_cell(y, x)
        # B 1 0
        # 1 1 0
        # 0 0 0
        self.ms.ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 1)
        self.assertEqual(self.ms.grid[0][0].marked, True)

    def test_mark_cells_basic_three(self):
        self.ms = MineSweeper(3, 3, 0)
        self.ms.add_mine(0, 0)
        self.ms.add_mine(0, 1)
        self.ms.add_mine(0, 2)
        for y in xrange(1, len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                self.ms.pick_cell(y, x)
        # B B B
        # 2 3 2
        # 0 0 0
        self.ms.ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 3)
        self.assertEqual(self.ms.grid[0][0].marked, True)
        self.assertEqual(self.ms.grid[0][1].marked, True)
        self.assertEqual(self.ms.grid[0][2].marked, True)

    def test_mark_cells_adjacents(self):
        self.ms = MineSweeper(3, 3, 0)
        self.ms.add_mine(0, 0)
        self.ms.pick_cell(0, 1)
        self.ms.pick_cell(1, 0)
        # Can't mark yet, not enough info! (could be 0,0 or 1,1)
        # B 1 ?
        # 1 ? ?
        # ? ? ?
        self.ms.ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 0)
        self.ms.add_mine(1, 1)
        # B 2 ?
        # 2 B ?
        # ? ? ?
        self.ms.ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 0)
        # Reveal top right, Adjacency should give us top left
        # B 2 1
        # 2 B ?
        # ? ? ?
        self.ms.pick_cell(0, 2)
        self.ms.ai.mark_cells()
        self.ms.display_grid()
        self.assertEqual(self.count_marked_cells(), 1)
        self.assertEqual(self.ms.grid[0][0].marked, True)

    def test_mark_cells_adjacents_two(self):
        # B ? B
        # 1 2 1
        # 0 0 0
        self.ms = MineSweeper(3, 3, 0)
        self.ms.add_mine(0, 0)
        self.ms.add_mine(0, 2)
        for y in xrange(1, len(self.ms.grid)):
            for x in xrange(len(self.ms.grid[0])):
                self.ms.pick_cell(y, x)
        self.ms.ai.mark_cells()
        self.assertEqual(self.count_marked_cells(), 2)
        self.assertEqual(self.ms.grid[0][0].marked, True)
        self.assertEqual(self.ms.grid[0][2].marked, True)
