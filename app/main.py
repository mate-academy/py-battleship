from typing import Any


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

        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:

        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        living_decks = [
            deck
            for deck in self.decks
            if deck.is_alive
        ]

        if not living_decks:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:

        self.field = {}

        for ship in ships:

            start, end = ship
            start_row, start_column = start
            end_row, end_column = end

            cells = []

            if start_row == end_row:
                for i in range(start_column, end_column + 1):
                    cells.append((start_row, i))
            elif start_column == end_column:
                for i in range(start_row, end_row + 1):
                    cells.append((i, start_column))

            self.field[tuple(cells)] = Ship(start, end)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        for cells, ship in self.field.items():
            if location in cells:
                row, column = location
                ship.fire(row, column)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        print()
        for row in range(10):
            line = ""
            for column in range(10):
                symbol = self.get_symbol(row, column)
                line += symbol
            print(f"{line}")

    def get_symbol(self, row: int, column: int) -> str:
        for cells, ship in self.field.items():
            if (row, column) in cells:
                if ship.is_drowned:
                    return "X"
                deck = ship.get_deck(row, column)
                if deck.is_alive:
                    return u"\u25A1"
                return "*"
        return "~"

    def _validate_field(self) -> None:

        if len(self.field) != 10:
            raise _FieldError("The total number of the ships should be 10")

        ships = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }
        for cells in self.field:
            ships[len(cells)] += 1
        if ships[4] != 1:
            raise _FieldError("There should be 4 single-deck ships")
        if ships[3] != 2:
            raise _FieldError("There should be 3 double-deck ships")
        if ships[2] != 3:
            raise _FieldError("There should be 2 three-deck ships")
        if ships[1] != 4:
            raise _FieldError("There should be 1 four-deck ship")

        empty_cells = []
        for cells in self.field:
            for cell in cells:
                row, column = cell
                self._add_new_cell(cells, empty_cells, row + 1, column)
                self._add_new_cell(cells, empty_cells, row - 1, column)
                self._add_new_cell(cells, empty_cells, row - 1, column + 1)
                self._add_new_cell(cells, empty_cells, row, column + 1)
                self._add_new_cell(cells, empty_cells, row + 1, column + 1)
                self._add_new_cell(cells, empty_cells, row + 1, column - 1)
                self._add_new_cell(cells, empty_cells, row, column - 1)
                self._add_new_cell(cells, empty_cells, row - 1, column - 1)
        empty_cells_set = set(empty_cells)
        for cells in self.field:
            for cell in cells:
                row, column = cell
                if (row, column) in empty_cells_set:
                    raise _FieldError("Ships shouldn't "
                                      "be located in the neighboring cells")

    @staticmethod
    def _add_new_cell(
            cells: tuple,
            checked_cells: list,
            row: int,
            column: int
    ) -> None:
        if ((row, column) not in cells
                and 9 >= row >= 0
                and 9 >= column >= 0):
            checked_cells.append((row, column))


class _FieldError(Exception):
    pass
