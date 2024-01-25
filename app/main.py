class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(row, col)
            for col in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple) -> str:
        for key in self.field:
            if (
                key[0][0] <= location[0] <= key[1][0]
                and key[0][1] <= location[1] <= key[1][1]
            ):
                self.field[key].fire(*location)
                if self.field[key].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
