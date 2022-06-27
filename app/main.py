import numpy as np


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.make_decks()
        self.length = 0
        if self.start[0] == self.end[0]:
            self.length = self.end[1] - self.start[1] + 1
        elif self.start[1] == self.end[1]:
            self.length = self.end[0] - self.start[0] + 1

    def make_decks(self):
        if self.start[0] == self.end[0]:
            for point in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], point))
        elif self.start[1] == self.end[1]:
            for point in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(point, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        damaged_deck = self.get_deck(row, column)
        damaged_deck.is_alive = False
        decks_hit_count = 0

        for deck in self.decks:
            if deck.is_alive is False:
                decks_hit_count += 1

        if decks_hit_count == self.length:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for coord in ships:
            new_ship = Ship(coord[0], coord[1])
            start = coord[0]
            end = coord[1]
            if start[0] == end[0]:
                for point in range(start[1], end[1] + 1):
                    self.field[start[0], point] = new_ship
            elif start[1] == end[1]:
                for point in range(start[0], end[0] + 1):
                    self.field[point, start[1]] = new_ship

    def fire(self, location: tuple):
        if location in self.field:
            damaged_ship = self.field[location]
            damaged_ship.fire(location[0], location[1])
            if damaged_ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self):
        """
        ~ - empty cell
        o - alive deck
        * - hit decks of the alive ship
        x - decks of the drowned ship
        """
        battlefield = np.zeros((10, 10), str)
        rows = battlefield.shape[0]
        columns = battlefield.shape[1]
        for i in range(0, rows):
            for j in range(0, columns):
                if (i, j) not in self.field:
                    battlefield[i, j] = "~"
                elif (i, j) in self.field:
                    if self.field[i, j].is_drowned:
                        battlefield[i, j] = "x"
                    else:
                        if Deck(i, j).is_alive:
                            battlefield[i, j] = "o"
                        battlefield[i, j] = "*"
        print(battlefield)
