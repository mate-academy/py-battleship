class Deck:
    def __init__(self, row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def create_deck(self) -> None:
        for i in range(self.start[1], self.end[1] + 1):
            self.decks.append(Deck(self.start[0], i))

    def get_deck(self, row: int, column: int) -> object:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        if fired_deck is not None:
            fired_deck.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self.ships = ships
        for value in self.field.values():
            value.create_deck()

    def fire(self, location: tuple) -> str:
        for ship, deck in self.field.items():
            if (location[0] in range(ship[0][0], ship[1][0] + 1)
                    and location[1] in range(ship[0][1], ship[1][1] + 1)):
                deck.fire(location[0], location[1])
                if deck.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
