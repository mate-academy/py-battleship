from typing import List, Tuple


class Battleship:
    """Class to represent a Battleship game field and simulate shots."""

    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        """
        Initialize the game field with given ships.

        :param ships: List of tuples representing ships by their end coordinates
        """
        self.size: int = 10
        self.field: List[List[str]] = [['~'] * self.size for _ in range(self.size)]
        self.ships: List[List[Tuple[int, int]]] = []
        self.hits: List[Tuple[int, int]] = []

        for start, end in ships:
            ship_cells = self._get_ship_cells(start, end)
            self.ships.append(ship_cells)
            for r, c in ship_cells:
                self.field[r][c] = '□'

        self._validate_field()

    def fire(self, cell: Tuple[int, int]) -> str:
        """
        Simulate a shot to the given cell.

        :param cell: Tuple of (row, column)
        :return: Result of the shot: "Miss!", "Hit!", or "Sunk!"
        """
        row, col = cell
        if self.field[row][col] == '~':
            return "Miss!"

        for ship in self.ships:
            if cell in ship:
                self.hits.append(cell)
                alive = [deck for deck in ship if deck not in self.hits]
                if alive:
                    self.field[row][col] = '*'
                    return "Hit!"
                else:
                    for r, c in ship:
                        self.field[r][c] = 'x'
                    return "Sunk!"

        return "Miss!"

    def print_field(self) -> None:
        """Print the current state of the field."""
        for row in self.field:
            print(' '.join(row))

    def _get_ship_cells(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Generate all cells occupied by a ship.

        :param start: Starting coordinate of the ship
        :param end: Ending coordinate of the ship
        :return: List of all cells occupied by the ship
        """
        cells = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                cells.append((start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                cells.append((row, start[1]))
        return cells

    def _validate_field(self) -> None:
        """Validate the field according to Battleship rules."""
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships.")

        lengths = [len(ship) for ship in self.ships]
        if lengths.count(1) != 4:
            raise ValueError("There must be 4 single-deck ships.")
        if lengths.count(2) != 3:
            raise ValueError("There must be 3 double-deck ships.")
        if lengths.count(3) != 2:
            raise ValueError("There must be 2 three-deck ships.")
        if lengths.count(4) != 1:
            raise ValueError("There must be 1 four-deck ship.")

        occupied = set()
        for ship in self.ships:
            for cell in ship:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = cell[0] + dr, cell[1] + dc
                        if (nr, nc) in occupied:
                            raise ValueError(
                                "Ships must not touch each other."
                            )
            occupied.update(ship)
