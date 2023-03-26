class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.decks = []
        self.is_drowned = False

    def get_deck(self, row, column) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def fire(self, row, column):
        for deck in self.decks:
            if deck[0] == row and deck[1] == column:
                deck.is_alive = False
        if len([deck.is_alive for deck in self.decks]) == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple):
        for ship in self.field:
            if location in ship:
                Ship(*ship).fire(*location)
                if Ship(*ship).is_drowned:
                    return "Sunk!"
                return "Hit!"
            return "Miss!"
