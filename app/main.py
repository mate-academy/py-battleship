class Battleship:
    def __init__(self, ships):
        self.size = 10
        self.field = [["~"] * self.size for _ in range(self.size)]
        self.ships = {}
        self.hits = set()

        for ship in ships:
            self._place_ship(ship)

        self._validate_field()

    def _place_ship(self, ship):
        (r1, c1), (r2, c2) = ship
        ship_cells = set()

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                self.field[r][c] = "□"
                ship_cells.add((r, c))

        self.ships[ship] = ship_cells

    def _validate_field(self):
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships!")

        ship_sizes = [len(cells) for cells in self.ships.values()]
        if ship_sizes.count(1) != 4 or ship_sizes.count(2) != 3 or \
                ship_sizes.count(3) != 2 or ship_sizes.count(4) != 1:
            raise ValueError("Invalid ship sizes!")

        if not self._check_no_adjacent_ships():
            raise ValueError("Ships should not be adjacent!")

    def _check_no_adjacent_ships(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        occupied = set()
        for cells in self.ships.values():
            occupied.update(cells)

        for r, c in occupied:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (nr, nc) in occupied and (nr, nc) not in self.ships:
                    return False
        return True

    def fire(self, cell):
        r, c = cell
        for ship, ship_cells in self.ships.items():
            if (r, c) in ship_cells:
                self.hits.add((r, c))
                if ship_cells.issubset(self.hits):
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self):
        display_field = [[self.field[r][c] for c in range(self.size)] for r in range(self.size)]

        for r, c in self.hits:
            display_field[r][c] = "*" if display_field[r][c] == "□" else "x"

        for row in display_field:
            print(" ".join(row))


