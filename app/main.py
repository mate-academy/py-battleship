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

        self.decks = []
        self._create_decks()

    def _create_decks(self) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self._create_field(ships)

    def _create_field(self, ships: list[int]) -> None:
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int]) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                deck.is_alive = False
                if all(not deck.is_alive for deck in ship.decks):
                    ship.is_drowned = True
                    return "Sunk!"
                else:
                    return "Hit!"
            else:
                return "Already Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].is_drowned:
                        print("x", end="\t")
                    elif not self.field[(row, column)].get_deck(
                            row,
                            column).is_alive:
                        print("*", end="\t")
                    else:
                        print("□", end="\t")
                else:
                    print("~", end="\t")
