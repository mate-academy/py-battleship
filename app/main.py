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
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive is True:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {}
        for coord in self.ships:
            self.field[(coord[0], coord[1])] = Ship(coord[0], coord[1])

    def fire(self, location: tuple):
        for ship in self.field.values():
            try:
                ship.fire(*location)
            except AttributeError:
                continue
            if ship.is_drowned is True:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
