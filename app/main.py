class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.decks = self.create_decks()
        self.is_drowned = False

    def create_decks(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck( row, column)
        if deck:
            deck.is_alive = False
            # if not any([deck.is_alive for deck in self.decks]):
            #     self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple):
        for ship in self.field:
            if Ship(*ship).get_deck(*location):
                Ship(*ship).fire(*location)
                if not any([deck.is_alive for deck in Ship(*ship).decks]):
                    Ship(*ship).is_drowned = True
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
