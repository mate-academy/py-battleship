class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self, start, end, is_drowned=False):
        self.is_downed = is_drowned
        self.decks = []
        self.length = 0

        for i in range(start[1], end[1] + 1):
            self.decks.append(Deck(start[0], i))
            self.length += 1

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column and deck.is_alive:
                return deck

            if row == deck.row \
                    and column == deck.column \
                    and deck.is_alive is False:
                if self.is_downed:
                    return "Sunk!"

    def fire(self, deck):
        deck.is_alive = False
        self.length -= 1

        if self.length == 0:
            self.is_downed = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for i in range(start[1], end[1] + 1):
                self.field[(start[0], i)] = ship

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            row, column = location
            deck = ship.get_deck(row, column)

            if deck == "Sunk!":
                return deck

            if deck.is_alive:
                return ship.fire(deck)

        return "Miss!"
