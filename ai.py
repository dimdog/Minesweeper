

class MinesweeperAI:

    def __init__(self, game):
        self.game = game
        self.completed = set()

    def mark_cells(self):
        """ Marks any known bombs."""
        marked = False
        print self.game.revealed
        for location in self.game.revealed:
            # location = (height, width)
            if location not in self.completed:  # if we've already done all we can with the spot
                height, width = location
                info = self.check_info(location)
                marked = info['marked']
                unknowns = info['unknowns']
                mines = self.game.grid[height][width].value
                if len(unknowns) == 0:
                    # nothing to do
                    self.completed.add(location)
                elif len(marked) + len(unknowns) == mines:
                    # if all the unknowns are mines
                    marked = True
                    for target in unknowns:
                        t_height, t_width = target
                        print "Marking {}".format(target)
                        self.game.grid[t_height][t_width].marked = True
                    self.completed.add(location)
        return marked

    def reveal_cell(self):
        """ picks a cell to reveal """
        revealed = False
        for location in self.game.revealed:
            # location = (height, width)
            if location not in self.completed:  # if we've already done all we can with the spot
                height, width = location
                info = self.check_info(location)
                marked = info['marked']
                unknowns = info['unknowns']
                mines = self.game.grid[height][width].value
                if len(unknowns) == 0:
                    # nothing to do...
                    self.completed.add(location)
                elif len(marked) == mines:
                    # time to reveal some cells...
                    return unknowns[0]

        return revealed

    def check_info(self, location):
        # returns {"unknowns": set((height,width)), "marked": set((height,width))}
        # input: location: (height, width)
        height, width = location
        unknowns = []
        marked = []
        for h in xrange(-1, 2):
            for w in xrange(-1, 2):
                if not (h == 0 and w == 0) and 0 <= height + h < self.game.height and 0 <= width + w < self.game.width:
                    if not self.game.grid[height + h][width + w].revealed:
                        if self.game.grid[height + h][width + w].marked:
                            marked.append((height + h, width + w))
                        else:
                            unknowns.append((height + h, width + w))
        return {"marked": marked, "unknowns": unknowns}



