class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> object:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if not deck.is_alive:
                self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
