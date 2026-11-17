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
        is_drowned: bool = False,
    ) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(
                min(start[0], end[0]),
                max(start[0], end[0]) + 1,
            )
            for column in range(
                min(start[1], end[1]),
                max(start[1], end[1]) + 1,
            )
            if start[0] == end[0] or start[1] == end[1]
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.ships = [Ship(*ship_data) for ship_data in ships]
        self.field: dict[tuple[int, int], Ship] = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        ship.fire(*location)
        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = []
            for column in range(10):
                ship = self.field.get((row, column))
                if ship is None:
                    line.append("~")
                elif ship.is_drowned:
                    line.append("x")
                elif ship.get_deck(row, column).is_alive:
                    line.append("□")
                else:
                    line.append("*")
            print("\t".join(line))

    def _validate_field(self) -> None:
        lengths = [len(ship.decks) for ship in self.ships]
        if sorted(lengths) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Wrong number of ships of each size")
        for (row, column), ship in self.field.items():
            for d_row in (-1, 0, 1):
                for d_column in (-1, 0, 1):
                    neighbor = self.field.get((row + d_row, column + d_column))
                    if neighbor is not None and neighbor is not ship:
                        raise ValueError("Ships must not be adjacent")
