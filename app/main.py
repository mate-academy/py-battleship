from typing import Dict, List, Set, Tuple


Cell = Tuple[int, int]
Ship = Tuple[Cell, Cell]


class Battleship:
    FIELD_SIZE: int = 10

    def __init__(self, ships: List[Ship]) -> None:
        self._ships_input: List[Ship] = ships
        self._ship_cells: Dict[Cell, int] = {}
        self._ships: Dict[int, Set[Cell]] = {}
        self._hits: Set[Cell] = set()

        self._create_field()
        self._validate_field()

    def _create_field(self) -> None:
        for ship_id, ship in enumerate(self._ships_input):
            start, end = ship
            row1, col1 = start
            row2, col2 = end

            if row1 != row2 and col1 != col2:
                raise ValueError(
                    "Ships must be horizontal or vertical"
                )

            cells: Set[Cell] = set()

            if row1 == row2:
                for col in range(
                    min(col1, col2),
                    max(col1, col2) + 1,
                ):
                    cells.add((row1, col))
            else:
                for row in range(
                    min(row1, row2),
                    max(row1, row2) + 1,
                ):
                    cells.add((row, col1))

            self._ships[ship_id] = cells

            for cell in cells:
                if cell in self._ship_cells:
                    raise ValueError("Ships overlap")

                self._ship_cells[cell] = ship_id

    def fire(self, ceil: Cell) -> str:
        if ceil not in self._ship_cells:
            return "Miss!"

        if ceil in self._hits:
            return "Miss!"

        ship_id = self._ship_cells[ceil]
        self._hits.add(ceil)
        self._ships[ship_id].remove(ceil)

        if not self._ships[ship_id]:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row_index in range(self.FIELD_SIZE):
            row_data: List[str] = []

            for col_index in range(self.FIELD_SIZE):
                cell = (row_index, col_index)

                if cell in self._ship_cells:
                    ship_id = self._ship_cells[cell]

                    if cell in self._hits:
                        if not self._ships[ship_id]:
                            row_data.append("x")
                        else:
                            row_data.append("*")
                    else:
                        row_data.append("□")
                else:
                    row_data.append("~")

            print(" ".join(row_data))

    def _validate_field(self) -> None:
        if len(self._ships_input) != 10:
            raise ValueError("There must be exactly 10 ships")

        lengths: List[int] = [
            len(cells) for cells in self._ships.values()
        ]

        if lengths.count(1) != 4:
            raise ValueError("There must be 4 single-deck ships")

        if lengths.count(2) != 3:
            raise ValueError("There must be 3 double-deck ships")

        if lengths.count(3) != 2:
            raise ValueError("There must be 2 three-deck ships")

        if lengths.count(4) != 1:
            raise ValueError("There must be 1 four-deck ship")

        all_cells: Set[Cell] = set(self._ship_cells.keys())

        for cell in all_cells:
            row, col = cell
            ship_id = self._ship_cells[cell]

            for delta_row in (-1, 0, 1):
                for delta_col in (-1, 0, 1):
                    if delta_row == 0 and delta_col == 0:
                        continue

                    neighbor = (
                        row + delta_row,
                        col + delta_col,
                    )

                    if (
                        0 <= neighbor[0] < self.FIELD_SIZE
                        and 0 <= neighbor[1] < self.FIELD_SIZE
                    ):
                        if (
                            neighbor in all_cells
                            and neighbor
                            not in self._ships[ship_id]
                        ):
                            raise ValueError(
                                "Ships cannot touch each other"
                            )
