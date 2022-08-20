class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    ships = {}

    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        else:
            if start[0] == end[0]:
                for i in range(start[1], end[1] + 1):
                    self.decks.append(Deck(start[0], i))
            if start[1] == end[1]:
                for i in range(start[0], end[0] + 1):
                    self.decks.append(Deck(i, start[1]))
        self.is_drowned = is_drowned
        Ship.ships[(start, end)] = self

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        for deck in self.decks:
            if self.get_deck(row, column) == deck:
                deck.is_alive = False
            if not any([deck.is_alive for deck in self.decks]):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            non_empty_cells = [(deck.row, deck.column)
                               for deck in Ship(ship[0], ship[1]).decks]
            for cell in non_empty_cells:
                self.field[cell] = Ship.ships[(ship[0], ship[1])]

    def fire(self, location: tuple):
        if location in list(self.field.keys()):
            self.field[location].fire(location[0], location[1])
            return "Sunk!" if self.field[location].is_drowned else "Hit!"
        return "Miss!"
