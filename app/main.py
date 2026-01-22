from typing import List, Tuple


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships_decks = []
        self.original_ships = []

        for start, end in ships:
            ship_coords = self._get_ship_coordinates(start, end)
            self.ships_decks.append(list(ship_coords))
            self.original_ships.append(list(ship_coords))
            for row, col in ship_coords:
                self.field[row][col] = u"\u25A1"

        if not self._validate_field(ships):
            raise ValueError("Invalid ship configuration")

    def _get_ship_coordinates(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[List[int]]:
        coords = []
        r_start, c_start = start
        r_end, c_end = end
        for row in range(min(r_start, r_end), max(r_start, r_end) + 1):
            for col in range(min(c_start, c_end), max(c_start, c_end) + 1):
                coords.append([row, col])
        return coords

    def fire(self, cell: Tuple[int, int]) -> str:
        row, col = cell
        target = [row, col]

        for index, ship in enumerate(self.ships_decks):
            if target in ship:
                self.field[row][col] = "*"
                ship.remove(target)
                if not ship:
                    for s_row, s_col in self.original_ships[index]:
                        self.field[s_row][s_col] = "x"
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))

    def _validate_field(
        self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> bool:
        if len(ships) != 10:
            return False
        lengths = []
        occupied_cells = set()
        for start, end in ships:
            coords = self._get_ship_coordinates(start, end)
            lengths.append(len(coords))
            for row, col in coords:
                for d_row in range(-1, 2):
                    for d_col in range(-1, 2):
                        neighbor = (row + d_row, col + d_col)
                        if neighbor in occupied_cells:
                            return False
            for row, col in coords:
                occupied_cells.add((row, col))
        return (
            lengths.count(1) == 4
            and lengths.count(2) == 3
            and lengths.count(3) == 2
            and lengths.count(4) == 1
        )
