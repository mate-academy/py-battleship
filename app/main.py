class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], start[1] + i)
                for i in range(end[1] - start[1] + 1)
            ]
        else:
            self.decks = [
                Deck(start[0] + i, start[1])
                for i in range(end[0] - start[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        for coordinates in ships:
            ship = Ship(*coordinates)
            filled_cells = tuple(
                [(deck.row, deck.column) for deck in ship.decks]
            )
            self.field.update({filled_cells: ship})

    def fire(self, location: tuple) -> None:
        for coordinates in self.field:
            if location in coordinates:
                self.field[coordinates].fire(*location)
                if self.field[coordinates].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
