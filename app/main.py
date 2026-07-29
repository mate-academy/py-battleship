class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.ships = {}
        self.hits = {}
        for ship in ships:
            start = ship[0]
            end = ship[1]
            if start[0] == end[0]:
                for col in range(start[1], end[1] + 1):
                    self.ships[(start[0], col)] = ship
            elif start[1] == end[1]:
                for row in range(start[0], end[0] + 1):
                    self.ships[(row, start[1])] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.ships:
            return "Miss!"

        ship = self.ships[location]

        if ship not in self.hits:
            self.hits[ship] = set()
        self.hits[ship].add(location)

        start = ship[0]
        end = ship[1]

        if start[0] == end[0]:
            size = abs(end[1] - start[1]) + 1
        else:
            size = abs(end[0] - start[0]) + 1

        if len(self.hits[ship]) == size:
            return "Sunk!"
        return "Hit!"

    def is_sunk(self, ship: tuple) -> int:
        start, end = ship
        if start[0] == end[0]:
            size = abs(end[1] - start[1]) + 1
        else:
            size = abs(end[0] - start[0]) + 1
        return len(self.hits[ship]) == size

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.ships.values():
            start, end = ship
            if start[0] == end[0]:
                row = start[0]
                for col in range(start[1], end[1] + 1):
                    if ship in self.hits and (row, col) in self.hits[ship]:
                        if self.is_sunk(ship):
                            field[row][col] = "x"
                        else:
                            field[row][col] = "*"
                    else:
                        field[row][col] = "□"
            elif start[1] == end[1]:
                col = start[1]
                for row in range(start[0], end[0] + 1):
                    if ship in self.hits and (row, col) in self.hits[ship]:
                        if self.is_sunk(ship):
                            field[row][col] = "x"
                        else:
                            field[row][col] = "*"
                    else:
                        field[row][col] = "□"

        for row in field:
            print(" ".join(row))

    def _get_ship_size(self, ship: tuple) -> int:
        start, end = ship
        if start[0] == end[0]:
            return abs(end[1] - start[1]) + 1
        return abs(end[0] - start[0]) + 1

    def _are_neighbors(self, pos1: int, pos2: int) -> int:
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    def _validate_field(self) -> bool:
        sizes = {}
        for ship in set(self.ships.values()):
            size = self._get_ship_size(ship)
            sizes[size] = sizes.get(size, 0) + 1

        if sizes != {1: 4, 2: 3, 3: 2, 4: 1}:
            return False

        all_cells = []
        for ship in self.ships.values():
            start, end = ship
            if start[0] == end[0]:
                row = start[0]
                for col in range(start[1], end[1] + 1):
                    all_cells.append((row, col))
            else:
                col = start[1]
                for row in range(start[0], end[0] + 1):
                    all_cells.append((row, col))

        for i, cell1 in enumerate(all_cells):
            for cell2 in all_cells[i + 1:]:
                if self._are_neighbors(cell1, cell2):
                    return False
        return True
