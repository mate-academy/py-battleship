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
        self.create_deck()
        pass

    def create_deck(self):
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

        elif self.start[1] == self.end[1]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if column == deck.column and row == deck.row:
                return deck

    def fire(self, row, column):
        deck_under_fire = self.get_deck(row, column)
        deck_under_fire.is_alive = False
        if True not in [deck.is_alive for deck in self.decks]:
            self.is_drowned = True
        pass


class Battleship:

    def __init__(self, ships):
        self.ships = ships
        self.field = {}
        self.create_ships()

    def create_ships(self):
        for coordinates in self.ships:
            x, y = coordinates
            ship = Ship(x, y)
            if x[0] == y[0]:
                for i in range(x[1], y[1] + 1):
                    self.field[(x[0], i)] = ship
            if x[1] == y[1]:
                for i in range(x[0], y[0] + 1):
                    self.field[(i, x[1])] = ship

    def fire(self, location: tuple):
        if location in self.field:
            row, column = location
            self.field[location].fire(row, column)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
