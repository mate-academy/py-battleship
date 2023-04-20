from typing import Optional


class Deck:
    def __init__(self, row: int, col: int, is_alive: bool = True) -> None:
        self.row = row
        self.col = col
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck(row={self.row}, col={self.col}, " \
               f"is_alive={self.is_alive})"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self._initialize_decks(start, end)

    def _initialize_decks(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        self.decks = [Deck(row_index, column_index)
                      for row_index in range(start[0], end[0] + 1)
                      for column_index in range(start[1], end[1] + 1)]

    def location(self) -> list:
        return [(deck.row, deck.column) for deck in self.decks]

    def get_deck(self, row: int, col: int) -> Optional[Deck]:
        return next(
            filter(
                lambda deck: deck.row == row and deck.col == col,
                self.decks
            ),
            None
        )

    def fire(self, row: int, col: int) -> None:
        deck = self.get_deck(row, col)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)

    def __repr__(self) -> str:
        return f"Ship(decks={self.decks}, is_drowned={self.is_drowned})"


class Battleship:
    def __init__(self, ships: Ship) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.col)] = ship

    def fire(self, location: list) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"


class GameBoard:
    EMPTY_SQUARE = "\t\t~"
    HIT_SQUARE = "\t\tx"
    SHIP_SQUARE = "\t\t\u25A1"
    MISS_SQUARE = "\t\t*"

    def __init__(self) -> None:
        self.field = self._create_empty_field()

    def _create_empty_field(self) -> list:
        return [[self.EMPTY_SQUARE] * 10 for _ in range(10)]

    def print_field(self) -> None:
        field = self._create_empty_field()
        for ship in self.field.values():
            points = ship.location()
            for row, column in points:
                if ship.is_drowned:
                    field[row][column] = self.HIT_SQUARE
                elif ship.get_deck(row, column):
                    field[row][column] = self.SHIP_SQUARE
                else:
                    field[row][column] = self.MISS_SQUARE
        for row in field:
            print("".join(row))


class PrintField:
    EMPTY_SQUARE = "\t\t~"
    HIT_SQUARE = "\t\tx"
    SHIP_SQUARE = "\t\t\u25A1"
    MISS_SQUARE = "\t\t*"

    def __init__(self) -> None:
        self.field = self._create_empty_field()

    def _create_empty_field(self) -> list:
        return [[self.EMPTY_SQUARE] * 10 for _ in range(10)]

    def print_field(self) -> None:
        field = self._create_empty_field()
        for ship in self.field.values():
            points = ship.location()
            for row, column in points:
                if ship.is_drowned:
                    field[row][column] = self.HIT_SQUARE
                elif ship.get_deck(row, column):
                    field[row][column] = self.SHIP_SQUARE
                else:
                    field[row][column] = self.MISS_SQUARE
        for row in field:
            print("".join(row))


class ValidateInput:
    SHIP_DECKS = {1: 4, 2: 3, 3: 2, 4: 1}
    SHIP_SIZE = {1: 1, 2: 2, 3: 3, 4: 4}

    def __init__(self) -> None:
        self.field = self._create_empty_field()
        self._validate_field()

    def _validate_field(self) -> None:
        total_ships = sum(self.SHIP_DECKS.values())
        if total_ships != 10:
            raise ValueError(f"Expected 10 ships, got {total_ships}")

        for size, count in self.SHIP_DECKS.items():
            if count != sum(ship.get_size() == size
                            for ship in self.field.values()):
                raise ValueError(f"Expected {count} "
                                 f"{self.SHIP_SIZE[size]}-deck ships")

        for ship in self.field.values():
            for row, col in ship.location():
                for r_offset in [-1, 0, 1]:
                    for c_offset in [-1, 0, 1]:
                        if (r_offset != 0 or c_offset != 0) and \
                                self.field.get((row + r_offset, col + c_offset)):
                            raise ValueError("Ships cannot be adjacent")
