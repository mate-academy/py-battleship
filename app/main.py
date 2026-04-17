class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships_data = []
        self.field = {}
        self.hits = set()
        self.sunk_ships = []

        for start, end in ships:
            ship_coords = self._generate_ship_coords(start, end)
            ship_index = len(self.ships_data)
            self.ships_data.append({"coords": ship_coords, "hits": 0})

            for coord in ship_coords:
                if coord in self.field:
                    raise ValueError("Ships cannot overlap!")
                self.field[coord] = ship_index

        self._validate_field()

    def _generate_ship_coords(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        row_start, col_start = start
        row_end, col_end = end

        # Validar que el barco sea una línea recta (horizontal o vertical)
        if row_start != row_end and col_start != col_end:
            raise ValueError("Ships must be straight lines!")

        coords = []
        for row in range(min(row_start, row_end), max(row_start, row_end) + 1):
            for col in range(
                min(col_start, col_end),
                max(col_start, col_end) + 1
            ):
                # Validar límites del tablero 10x10
                if not (0 <= row <= 9 and 0 <= col <= 9):
                    raise ValueError("Ship coordinates out of bounds!")
                coords.append((row, col))
        return coords

    def fire(self, cell: tuple[int, int]) -> str:
        row, col = cell
        # Validar límites del disparo
        if not (0 <= row <= 9 and 0 <= col <= 9):
            return "Miss!"

        if cell not in self.field:
            return "Miss!"

        ship_idx = self.field[cell]
        ship = self.ships_data[ship_idx]

        # Solo incrementamos hits si es una celda nueva
        if cell not in self.hits:
            self.hits.add(cell)
            ship["hits"] += 1

        if ship["hits"] == len(ship["coords"]):
            if ship_idx not in self.sunk_ships:
                self.sunk_ships.append(ship_idx)
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for col in range(10):
                coord = (row, col)
                if coord not in self.field:
                    row_str += "~ "
                elif coord in self.hits:
                    ship_idx = self.field[coord]
                    sym = "x " if ship_idx in self.sunk_ships else "* "
                    row_str += sym
                else:
                    row_str += "□ "
            print(row_str.strip())

    def _validate_field(self) -> None:
        if len(self.ships_data) != 10:
            raise ValueError("Must have exactly 10 ships")

        lengths = [len(s["coords"]) for s in self.ships_data]
        counts = {i: lengths.count(i) for i in range(1, 5)}
        if counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid ship sizes distribution")

        for row, col in self.field:
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    if d_row == 0 and d_col == 0:
                        continue
                    neighbor = (row + d_row, col + d_col)
                    if neighbor in self.field:
                        if self.field[neighbor] != self.field[(row, col)]:
                            raise ValueError("Ships are too close!")
