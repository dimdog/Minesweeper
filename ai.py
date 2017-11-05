from random import Random
random = Random()


class MinesweeperAI:

    def __init__(self, game):
        self.game = game
        self.completed = set()

    def mark_cells(self):
        """ Marks any known bombs."""
        # print "Beginning Marking pass"
        # print "\tCompleted RN:{}".format(self.completed)
        for location in self.game.revealed:
            # location = (height, width)
            if location not in self.completed:  # if we've already done all we can with the spot
                height, width = location
                info = self.check_info(location)
                marked = info['marked']
                unknowns = info['unknowns']
                adjacents = info['adjacents']
                mines = self.game.grid[height][width].value
                remaining_mines = mines - len(marked)
                if len(unknowns) == 0:
                    # nothing to do
                    self.completed.add(location)
                elif len(unknowns) == remaining_mines:
                    # if all the unknowns are mines
                    for target in unknowns:
                        self.game.mark_cell(*target)
                    self.completed.add(location)
                else:  # check adjacency
                    for adjacent in adjacents:
                        if adjacent not in self.completed:
                            other_info = self.check_info(adjacent)
                            if len(other_info['unknowns']) == 0:
                                self.completed.add(adjacent)
                            else:
                                other_mines = self.game.grid[adjacent[0]][adjacent[1]].value
                                other_remaining_mines = other_mines - len(other_info['marked'])
                                if other_remaining_mines > remaining_mines:
                                    self.mark_adjacency(other_info, other_remaining_mines, info, remaining_mines)
                                elif remaining_mines > other_remaining_mines:
                                    self.mark_adjacency(info, remaining_mines, other_info, other_remaining_mines)

    def mark_adjacency(self, info_a, mines_a, info_b, mines_b):
        """ 'a' is guaranteed to have at least as many mines as 'b'"""
        a_unknowns = set(info_a['unknowns'])
        b_unknowns = set(info_b['unknowns'])
        difference = a_unknowns - b_unknowns
        if len(difference) == mines_a - mines_b:
            for location in difference:
                self.game.mark_cell(*location)

    def reveal_adjacency(self, info_a, mines_a, info_b, mines_b):
        """ 'a' is guaranteed to have more unknowns and equal or greater mines than 'b'"""
        a_unknowns = set(info_a['unknowns'])
        b_unknowns = set(info_b['unknowns'])
        if len(b_unknowns - a_unknowns) == 0:
            difference = a_unknowns - b_unknowns
            for location in difference:
                print "Adjacency Guess: A Mines:{}\tB Mines:{}\n\tA Unknowns:{}\n\tB Unknowns{}".format(mines_a, mines_b, a_unknowns, b_unknowns)
                return location

    def reveal_cell(self):
        """ picks a cell to reveal """
        best_odds_dict = {}
        for location in self.game.revealed:
            # location = (height, width)
            if location not in self.completed:  # if we've already done all we can with the spot
                height, width = location
                info = self.check_info(location)
                marked = info['marked']
                unknowns = info['unknowns']
                adjacents = info['adjacents']
                mines = self.game.grid[height][width].value
                remaining_mines = mines - len(marked)
                if len(unknowns) == 0:
                    # nothing to do...
                    self.completed.add(location)
                elif remaining_mines == 0:
                    # time to reveal some cells...
                    return unknowns[0]
                else:
                    # check adjacents, try to see if we can be certain...
                    """ 'a' is guaranteed to have more unknowns and equal or greater mines than 'b'"""
                    for adjacent in adjacents:
                        other_info = self.check_info(adjacent)
                        if len(other_info['unknowns']) == 0:
                            self.completed.add(adjacent)
                        else:
                            print "\tA:{}\tB:{}".format(location, adjacent)
                            other_mines = self.game.grid[adjacent[0]][adjacent[1]].value
                            other_remaining_mines = other_mines - len(other_info['marked'])
                            move = None
                            if remaining_mines >= other_remaining_mines:
                                if len(unknowns) > len(other_info['unknowns']):
                                    move = self.reveal_adjacency(info, remaining_mines, other_info, other_remaining_mines)
                                elif len(unknowns) < len(other_info['unknowns']) and remaining_mines == other_remaining_mines:
                                    move = self.reveal_adjacency(other_info, other_remaining_mines, info, remaining_mines)
                            else:
                                if len(unknowns) < len(other_info['unknowns']):
                                    move = self.reveal_adjacency(other_info, other_remaining_mines, info, remaining_mines)
                            if move:
                                return move

                    # now we have to guess, lets see if we can make a good guess
                    odds = float(mines - len(marked)) / float(len(unknowns))
                    for cell in unknowns:
                        cell_str = "{},{}".format(cell[0], cell[1])
                        if cell_str not in best_odds_dict or odds > best_odds_dict[cell_str]:
                            best_odds_dict["{},{}".format(cell[0], cell[1])] = odds
        # if we are here, then we are just guessing...
        mines_left = len(self.game.mines) - len(self.game.marked)
        squares_left = len(self.game.hidden)
        prob_per_square = float(mines_left) / float(squares_left)
        print "Odds: Mines left:{} Unknown Squares:{}, liklihood / square:{}".format(mines_left, squares_left, prob_per_square)
        # best odds we can have - short of 0 - is a 1 surrounded by 9 unknowns. - an 11% chance
        # random cell after picking first is 20% chance.
        best_odds_location = None
        best_odds = prob_per_square  # this is before we start getting clever with adjacency
        for key, value in best_odds_dict.items():
            height, width = [int(k) for k in key.split(",")]
            if value < best_odds:
                best_odds = value
                best_odds_location = (height, width)
        if best_odds_location:
            print "Guessing {}, odds:{}".format(best_odds_location, best_odds)
        else:
            print "Random Guess"
        return best_odds_location or list(self.game.hidden)[random.randint(0, len(self.game.hidden) - 1)]

    def check_info(self, location):
        # returns {"unknowns": set((height,width)), "marked": set((height,width), "adjacents": set((height,width))}
        # input: location: (height, width)
        height, width = location
        unknowns = []
        marked = []
        adjacents = []
        for h in xrange(-1, 2):
            for w in xrange(-1, 2):
                if not (h == 0 and w == 0) and 0 <= height + h < self.game.height and 0 <= width + w < self.game.width:
                    if not self.game.grid[height + h][width + w].revealed:
                        if self.game.grid[height + h][width + w].marked:
                            marked.append((height + h, width + w))
                        else:
                            unknowns.append((height + h, width + w))
                    else:
                        adjacents.append((height + h, width + w))
        return {"marked": marked, "unknowns": unknowns, "adjacents": adjacents}



