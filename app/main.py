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
        self.decks = self.design_decks(self.start, self.end)
        self.count_of_hit = 0

    @staticmethod
    def design_decks(start, end):
        if start == end:
            return [Deck(*start)]
        if start[0] == end[0]:
            return [
                Deck(start[0], deck)
                for deck in range(start[1], end[1] + 1)
            ]
        if start[1] == end[1]:
            return [
                Deck(deck, start[1])
                for deck in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        alive = [deck.is_alive for deck in self.decks]

        if any(alive):
            return "Hit!"
        else:
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list):
        self.ships = ships
        self.field = {ship: Ship(*ship) for ship in self.ships}

    def fire(self, location: tuple):
        for ship in self.field.values():
            for deck in ship.decks:
                if location[0] == deck.row and location[1] == deck.column:
                    return ship.fire(*location)

        return "Miss!"
