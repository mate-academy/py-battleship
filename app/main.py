class Deck:
    def __init__(self, row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int,
                 is_drowned: bool = False) -> None:
        self.decks = [Deck(row, column) for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        return next((deck for deck in self.decks if deck.row
                     == row and deck.column == column), None)

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {
            (deck.row, deck.column):
                ship for ship in [Ship(start, end)
                                  for start, end in ships]
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship:
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _is_sunk(self, ceil: tuple) -> bool:
        for ship in self.ships:
            if (ceil in ship
                    and all(self.field[row][column]
                            == "*" for row, column in ship)):
                return True
        return False

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
        print()

    def _validate_field(self) -> None:
        ship_counts = [0, 4, 3, 2, 1]
        for ship in self.ships:
            ship_len = len(ship)
            assert ship_len in [1, 2, 3, 4], f"Invalid ship length: {ship_len}"
            ship_counts[ship_len] -= 1
            for row, column in ship:
                for point_x in range(max(0, row - 1), min(10, row + 2)):
                    for point_y in range(max(0, column - 1),
                                         min(10, column + 2)):
                        if ((point_x, point_y) not in ship
                                and self.field[point_x][point_y] != "~"):
                            raise ValueError("Ships are too close")
        assert all(count == 0 for count in ship_counts), ("Invalid "
                                                          "number of ships")
