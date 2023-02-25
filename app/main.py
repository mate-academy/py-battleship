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
    def __init__(
            self,
            start: list[int],
            end: list[int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row=row, column=column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row=row, column=column).is_alive = False
        alive_deck = [deck.is_alive for deck in self.decks]

        if any(alive_deck):
            return "Hit!"

        self.is_drowned = True

        return "Sunk!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = tuple(
            Ship(
                start=ship_start, end=ship_end
            )
            for ship_start, ship_end in self.ships
        )

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            if ship.get_deck(*location):
                return ship.fire(*location)

        return "Miss!"
