from random import Random
random = Random()


class MineSweeper:
    def __init__(self, height=10, width=20, mines=99):
        grid_size = height*width
        self.grid = []
        for h in xrange(height):
            grid_row = [0]*width
            self.grid.append(grid_row)

        for i in xrange(mines):
            mine_loc = random.randint(0, grid_size-1)
            mine_height = mine_loc / height
            mine_width = (mine_loc - mine_height * height) % width
            self.add_mine(mine_height, mine_width)

        print self.grid

    def add_mine(self, mine_height, mine_width):
        self.grid[mine_height][mine_width] = -1
        for h in xrange(-1, 2):  # -1 to 1
            for w in xrange(-1, 2):  # -1 to 1
                if not (h == 0 and w == 0) and 0 <= mine_height + h < len(self.grid) and 0 <= mine_width + w < len(self.grid[0]):
                    self.grid[mine_height + h][mine_width + w] += 1

MineSweeper(5, 5, 1)
