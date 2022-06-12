class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.col = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        self._create_ship(start, end)

    def _create_ship(self, start, end):
        if start[0] == end[0]:
            for column in (range(start[1], end[1] + 1)):
                self.decks.append(Deck(start[0], column))
        else:
            for row in (range(start[0], end[0] + 1)):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.col:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[deck.row, deck.col] = ship

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

