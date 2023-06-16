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
    def __init__(self, ships: list) -> None:
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


if __name__ == '__main__':
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )
    print(battle_ship.fire((0, 4)))