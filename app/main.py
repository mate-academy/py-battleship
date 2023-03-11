class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for column in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        crush_deck = self.get_deck(row, column)
        if crush_deck:
            crush_deck.is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.ship = Ship(*ship)
            for deck in self.ship.decks:
                self.field[deck.row, deck.column] = self.ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        else:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
