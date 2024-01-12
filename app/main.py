class Deck:
    def __init__(self, row: int, column: int, is_alive: str = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple, end: tuple,
            is_drowned: str = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = (
            [Deck(row, column) for row in range(start[0], end[0] + 1)
             for column in range(start[1], end[1] + 1)]
        )

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck:
            target_deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {}
        for ship_position in ships:
            ship = Ship(*ship_position)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(*location)
                    if not deck.is_alive:
                        print("x", end=" ")
                    elif not ship.is_drowned:
                        print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
