from random import Random
random = Random()


class MinesweeperAI:

    def __init__(self, game):
        self.game = game
        self.completed = set()

    def mark_cells(self):
        """ Marks any known bombs."""
        marked = False
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
        mines_left = len(self.game.mines) - len(self.game.marked)
        squares_left = len(self.game.hidden)
        prob_per_square = float(mines_left) / float(squares_left)
        print "Odds: Mines left:{} Unknown Squares:{}, liklihood / square:{}".format(mines_left, squares_left, prob_per_square * 100)
        # best odds we can have - short of 0 - is a 1 surrounded by 9 unknowns. - an 11% chance
        # random cell after picking first is 20% chance.
        best_odds = prob_per_square  # this is before we start getting clever with adjacency
        best_odds_location = None
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
                else:
                    odds = float(mines - len(marked)) / float(len(unknowns))
                    if odds < best_odds:
                        best_odds = odds
                        best_odds_location = unknowns[0]
        # if we are here, then we are just guessing...

        return best_odds_location or list(self.game.hidden)[random.randint(0, len(self.game.hidden) - 1)]

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



