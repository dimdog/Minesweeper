from random import Random
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

    def __init__(self, height=10, width=20, mines=99):
        self.grid = []
        self.game_over = False
        self.reset(height, width, mines)

    def reset(self, height, width, mines):
        grid_size = height * width
        self.grid = []
        self.game_over = False
        for h in xrange(height):
            grid_row = []
            for w in xrange(width):
                grid_row.append(Cell(0))
            self.grid.append(grid_row)

        for i in xrange(mines):
            mine_loc = random.randint(0, grid_size - 1)
            mine_height = mine_loc / height
            mine_width = (mine_loc - mine_height * height) % width
            self.add_mine(mine_height, mine_width)

    def add_mine(self, mine_height, mine_width):
        self.grid[mine_height][mine_width].value = -1
        for h in xrange(-1, 2):  # -1 to 1
            for w in xrange(-1, 2):  # -1 to 1
                if not (h == 0 and w == 0) and 0 <= mine_height + h < len(self.grid) and 0 <= mine_width + w < len(self.grid[0]):
                    self.grid[mine_height + h][mine_width + w].value += 1

    def display_grid(self):
        print "Minesweeper"
        print "-" * 40
        for row in self.grid:
            print ("{}, " * len(row)).format(*[cell for cell in row])
        print "-" * 40

    def validate_cell(self, width, height):
        if height < 0 or height > len(self.grid) or width < 0 or width > len(self.grid[height]):
            return False
        if self.game_over or self.grid[height][width].revealed:
            return False
        return True

    def mark_cell(self, width, height):
        if not self.validate_cell(width, height):
            return False
        self.grid[height][width].marked = True

    def pick_cell(self, width, height):
        if not self.validate_cell(width, height):
            return False
        self.game_over = self.grid[height][width].value == -1
        self.grid[height][width].revealed = True
        return not self.game_over

    def game_loop(self):
        while not self.game_over:
            self.display_grid()
            print "Mark(M) or Guess(G)?"
            decision = raw_input()
            decision = decision.upper()
            if decision not in {"M", "G"}:
                continue
            if decision == "M":
                "Marking..."
            else:
                "Guessing..."
            print "Height of target cell?"
            height = raw_input()
            print "Width of target cell?"
            width = raw_input()
            if decision == "G":
                self.pick_cell(int(width), int(height))
            else:
                self.mark_cell(int(width), int(height))
        print "BOOM"
        self.display_grid()


if __name__ == "__main__":
    m = MineSweeper(5, 5, 1)
    m.game_loop()


