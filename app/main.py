from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List, Set, Tuple

BOARD_SIZE: int = 10

Coordinate = Tuple[int, int]
ShipEnds = Tuple[Coordinate, Coordinate]

WATER_CELL: str = "~"
SHIP_CELL: str = "□"
HIT_CELL: str = "*"
SUNK_CELL: str = "x"


def _coords_between(
    start_point: Coordinate,
    end_point: Coordinate,
) -> List[Coordinate]:
    """Return all coordinates between two endpoints (inclusive)."""
    (row_start, col_start), (row_end, col_end) = start_point, end_point

    if row_start == row_end:
        column_from, column_to = sorted((col_start, col_end))
        return [
            (row_start, column_index)
            for column_index in range(column_from, column_to + 1)
        ]

    if col_start == col_end:
        row_from, row_to = sorted((row_start, row_end))
        return [
            (row_index, col_start)
            for row_index in range(row_from, row_to + 1)
        ]

    raise ValueError("Ship must be horizontal or vertical")


class Battleship:
    def __init__(self, ships: Iterable[ShipEnds]) -> None:
        self.field: List[List[str]] = [
            [WATER_CELL for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]
        self.ships_info: Dict[int, Dict[str, Set[Coordinate]]] = {}
        self.coord_to_ship: Dict[Coordinate, int] = {}

        for ship_id, ship_ends in enumerate(ships):
            self._add_ship(ship_id, ship_ends)

        self._validate_field()

    def fire(self, cell: Coordinate) -> str:
        row_index, column_index = cell
        self._validate_coordinate(row_index, column_index)

        ship_id = self.coord_to_ship.get((row_index, column_index))
        if ship_id is None:
            return "Miss!"

        ship_info = self.ships_info[ship_id]
        if (row_index, column_index) not in ship_info["alive"]:
            return "Miss!"

        ship_info["alive"].remove((row_index, column_index))
        self.field[row_index][column_index] = HIT_CELL

        if not ship_info["alive"]:
            self._mark_sunk(ship_info["all"])
            return "Sunk!"

        return "Hit!"

    def _add_ship(self, ship_id: int, ends: ShipEnds) -> None:
        (row_start, col_start), (row_end, col_end) = ends
        ship_cells = _coords_between(
            (row_start, col_start),
            (row_end, col_end),
        )

        all_cells = set(ship_cells)
        self.ships_info[ship_id] = {
            "all": all_cells,
            "alive": set(all_cells),
        }

        for row_index, column_index in ship_cells:
            self._validate_coordinate(row_index, column_index)

            if (row_index, column_index) in self.coord_to_ship:
                raise ValueError("Ships are overlapping")

            self.coord_to_ship[(row_index, column_index)] = ship_id
            self.field[row_index][column_index] = SHIP_CELL

    def _validate_field(self) -> None:
        ship_lengths = [
            len(info["all"])
            for info in self.ships_info.values()
        ]

        if len(ship_lengths) != 10:
            raise ValueError("There must be exactly 10 ships")

        ship_count = Counter(ship_lengths)
        expected_config = {1: 4, 2: 3, 3: 2, 4: 1}

        for length, required_count in expected_config.items():
            actual_count = ship_count.get(length, 0)
            if actual_count != required_count:
                raise ValueError(
                    f"Expected {required_count} ships of length {length}, "
                    f"found {actual_count}",
                )

        for ship_id, ship_info in self.ships_info.items():
            for row_index, column_index in ship_info["all"]:
                self._validate_no_adjacent_ships(
                    ship_id=ship_id,
                    row_index=row_index,
                    column_index=column_index,
                )

    def _validate_no_adjacent_ships(
        self,
        ship_id: int,
        row_index: int,
        column_index: int,
    ) -> None:
        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                if delta_row == 0 and delta_col == 0:
                    continue

                neighbour_row = row_index + delta_row
                neighbour_col = column_index + delta_col

                if not (
                    0 <= neighbour_row < BOARD_SIZE
                    and 0 <= neighbour_col < BOARD_SIZE
                ):
                    continue

                other_ship = self.coord_to_ship.get(
                    (neighbour_row, neighbour_col),
                )
                if other_ship is None:
                    continue

                if other_ship != ship_id:
                    raise ValueError("Ships are adjacent or overlapping")

    def _validate_coordinate(self, row_index: int, column_index: int) -> None:
       if not (
    0 <= row_index < BOARD_SIZE
    and 0 <= column_index < BOARD_SIZE
    ):
            raise ValueError("Coordinates out of range")

    def _mark_sunk(self, ship_cells: Set[Coordinate]) -> None:
        for row_index, column_index in ship_cells:
            self.field[row_index][column_index] = SUNK_CELL

    def render_field(self) -> List[str]:
        return ["\t".join(row) for row in self.field]

    def print_field(self) -> None:
        for line in self.render_field():
            print(line)
