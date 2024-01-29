class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.create_deck()

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


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {}
        self.create_ships()

    def create_ships(self):
        for coordinate in self.ships:
            start, end = coordinate
            ship = Ship(start, end)
            if start[0] == end[0]:
                for i in range(start[1], end[1] + 1):
                    self.field[(start[0], i)] = ship
            if start[1] == end[1]:
                for i in range(start[0], end[0] + 1):
                    self.field[(i, start[1])] = ship

    def fire(self, location: tuple):
        if location in self.field:
            row, column = location
            self.field[location].fire(row, column)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
