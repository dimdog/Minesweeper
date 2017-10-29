from random import Random
from ai import MinesweeperAI
random = Random()


class Cell:
    def __init__(self, value):
        self.value = value
        self.revealed = False
        self.marked = False

    def __repr__(self):
        if self.revealed:
            return str(self.value)
        if self.marked:
            return "M"
        return "?"


class MineSweeper:

    def __init__(self, height=16, width=30, mines=99):
        self.grid = []
        self.mines = set()
        self.revealed = set()
        self.hidden = set()
        self.marked = set()
        self.game_over = False
        self.height = height
        self.width = width
        self.reset(height, width, mines)
        self.total_non_mines = height * width - mines
        self.ai = MinesweeperAI(self)

    def reset(self, height, width, mines):
        self.grid = []
        self.game_over = False
        for h in xrange(height):
            grid_row = []
            for w in xrange(width):
                grid_row.append(Cell(0))
                self.hidden.add((h, w))
            self.grid.append(grid_row)
        while len(self.mines) < mines:
            mine_height = random.randint(0, height - 1)
            mine_width = random.randint(0, width - 1)
            self.add_mine(mine_height, mine_width)

    def add_mine(self, mine_height, mine_width):
        if (mine_height, mine_width) in self.mines:
            return False
        self.grid[mine_height][mine_width].value = -1
        for h in xrange(-1, 2):  # -1 to 1
            for w in xrange(-1, 2):  # -1 to 1
                if not (h == 0 and w == 0) and 0 <= mine_height + h < len(self.grid) and 0 <= mine_width + w < len(self.grid[0]) and \
                        self.grid[mine_height + h][mine_width + w].value != -1:
                    self.grid[mine_height + h][mine_width + w].value += 1
        self.mines.add((mine_height, mine_width))
        return True

    def display_grid(self):
        print "Minesweeper"
        print "-" * 40
        for row in self.grid:
            print ("{}, " * len(row)).format(*[cell for cell in row])
        print "-" * 40

    def validate_cell(self, width, height):
        if height < 0 or height >= len(self.grid) or width < 0 or width >= len(self.grid[height]):
            return False
        if self.game_over or self.grid[height][width].revealed:
            return False
        return True

    def mark_cell(self, width, height):
        if not self.validate_cell(width, height):
            return False
        self.grid[height][width].marked = not self.grid[height][width].marked
        self.marked.add((height, width))
        self.hidden.discard((height, width))
        return True

    def pick_cell(self, width, height):
        if not self.validate_cell(width, height):
            return False
        self.game_over = self.grid[height][width].value == -1
        self.grid[height][width].revealed = True
        self.revealed.add((height, width))
        self.hidden.discard((height, width))
        if self.grid[height][width].value == 0:
            self.reveal_surrounding_empty_cells(width, height)
        return not self.game_over

    def reveal_surrounding_empty_cells(self, width, height):
        """ the gist is that the cell at width, height is a 0, so lets reveal all the cells around it.
        All the 0's it is touching get the same treatment """
        for h in xrange(-1, 2):  # -1 to 1
            for w in xrange(-1, 2):  # -1 to 1
                if not (h == 0 and w == 0) and 0 <= height + h < len(self.grid) and 0 <= width + w < len(self.grid[0]):
                    if self.grid[height + h][width + w].value == 0 and not self.grid[height + h][width + w].revealed:
                        self.grid[height + h][width + w].revealed = True
                        self.reveal_surrounding_empty_cells(width + w, height + h)
                    self.grid[height + h][width + w].revealed = True
                    self.revealed.add((height + h, width + w))
                    self.hidden.discard((height + h, width + h))

    def game_loop(self):
        while not self.game_over:
            self.display_grid()
            print "Mark(M) or Guess(G) or AI Guess(A)?"
            decision = raw_input()
            decision = decision.upper()
            if decision not in {"M", "G", "A"}:
                continue
            if decision == "M":
                "Marking..."
            else:
                "Guessing..."
            if decision in {"M", "G"}:
                print "Height of target cell?"
                height = raw_input()
                print "Width of target cell?"
                width = raw_input()
            if decision == "G":
                self.pick_cell(int(width), int(height))
            elif decision == "M":
                self.mark_cell(int(width), int(height))
            else:  # AI Decision
                self.ai.mark_cells()
                pick = self.ai.reveal_cell()
                print pick
                if pick:
                    height, width = pick
                    self.pick_cell(width, height)
            if len(self.revealed) == self.total_non_mines:
                break

        if self.game_over:
            print "BOOM"
        else:
            print "You Win!"
        self.display_grid()


if __name__ == "__main__":
    m = MineSweeper()
    m.game_loop()


