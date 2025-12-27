from typing import List, Tuple, Dict


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships = ships
        self.field: List[List[str]] = [
            ["~" for _ in range(10)] for _ in range(10)
        ]
        self.ship_cells: Dict[
            Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]
        ] = {}
        self._place_ships()
        self._validate_field()

    def _place_ships(self) -> None:
        for ship in self.ships:
            (start_row, start_col), (end_row, end_col) = ship
            if start_row == end_row:  # Horizontal ship
                for col in range(start_col, end_col + 1):
                    self.field[start_row][col] = "□"
                    self.ship_cells[(start_row, col)] = ship
            elif start_col == end_col:  # Vertical ship
                for row in range(start_row, end_row + 1):
                    self.field[row][start_col] = "□"
                    self.ship_cells[(row, start_col)] = ship

    def fire(self, cell: Tuple[int, int]) -> str:
        row, col = cell
        if self.field[row][col] == "~":
            return "Miss!"
        elif self.field[row][col] == "□":
            self.field[row][col] = "*"
            ship = self.ship_cells[cell]
            if all(
                self.field[ship_row][ship_col] == "*"
                for ship_row, ship_col in self._get_ship_cells(ship)
            ):
                for ship_row, ship_col in self._get_ship_cells(ship):
                    self.field[ship_row][ship_col] = "x"
                return "Sunk!"
            return "Hit!"

    def _get_ship_cells(
        self, ship: Tuple[Tuple[int, int], Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        (start_row, start_col), (end_row, end_col) = ship
        if start_row == end_row:
            return [(start_row, col) for col in range(start_col, end_col + 1)]
        elif start_col == end_col:
            return [(row, start_col) for row in range(start_row, end_row + 1)]
        return []

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        ship_lengths = [len(self._get_ship_cells(ship)) for ship in self.ships]
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships.")
        if ship_lengths.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships.")
        if ship_lengths.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships.")
        if ship_lengths.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships.")
        if ship_lengths.count(4) != 1:
            raise ValueError("There should be 1 four-deck ship.")
        if not self._check_no_adjacent_ships():
            raise ValueError(
                "Ships shouldn't be located in neighboring cells."
            )

    def _check_no_adjacent_ships(self) -> bool:
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for (row, col) in self.ship_cells:
            for dr, dc in directions:
                adjacent_row, adjacent_col = row + dr, col + dc
                if (
                        0 <= adjacent_row < 10
                        and 0 <= adjacent_col < 10
                        and self.field[adjacent_row][adjacent_col] == "□"
                        and (adjacent_row, adjacent_col) not in self.ship_cells
                ):
                    return False
        return True
