class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if self.start[0] == self.end[0]:
            self.decks = [Deck(self.start[0], column) for column
                          in range(self.start[1], self.end[1] + 1)]
        if self.start[1] == self.end[1]:
            self.decks = [Deck(row, self.start[1]) for row
                          in range(self.start[0], self.end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck in self.decks and deck.is_alive:
            deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return "Hit!"
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            self.field[(ship.start, ship.end)] = ship

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            for deck in ship.decks:
                if (deck.row, deck.column) == location:
                    row, column = location
                    return ship.fire(row, column)
        return "Miss!"
