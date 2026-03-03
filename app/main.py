from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(
            self,
            start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.decks: List[Deck] = []
        self.is_drowned = False
        self._create_decks()

    def _create_decks(self) -> None:
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def fire(self, row: int, col: int) -> str:
        # Check if this cell matches a deck
        for deck in self.decks:
            if deck.row == row and deck.column == col:
                deck.hit()
                if all(not d.is_alive for d in self.decks):
                    self.is_drowned = True
                return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []
        self._validate_field(ships)
        self._place_ships(ships)

    def _place_ships(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        # Place the ships on the field and store them
        for ship_coords in ships:
            start, end = ship_coords
            # First, check if the ship is adjacent to any other ship
            if self._check_adjacent_cells(start, end):
                raise ValueError("Ships cannot be in neighboring cells.")
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        ship_sizes = {1: 4, 2: 3, 3: 2, 4: 1}
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship_coords in ships:
            start, end = ship_coords
            if start[0] == end[0]:
                size = end[1] - start[1] + 1
            elif start[1] == end[1]:
                size = end[0] - start[0] + 1
            else:
                raise ValueError("Ships must be either "
                                 "horizontal or vertical.")

            if size not in ship_counts:
                raise ValueError("Invalid ship size.")
            ship_counts[size] += 1

        # Check if the ship sizes match the expected counts
        for size, count in ship_counts.items():
            if count != ship_sizes[size]:
                raise ValueError(f"Invalid number of ships with {size} decks.")

    def _get_adjacent_cells(
            self,
            start: Tuple[int, int], end: Tuple[int, int]) -> set:
        adjacent_cells = set()

        if start[0] == end[0]:
            for row in range(start[0] - 1, start[0] + 2):
                for col in range(start[1] - 1, end[1] + 2):
                    adjacent_cells.add((row, col))
        elif start[1] == end[1]:  # Vertical ship
            for row in range(start[0] - 1, end[0] + 2):
                for col in range(start[1] - 1, start[1] + 2):
                    adjacent_cells.add((row, col))

        return adjacent_cells

    def _check_adjacent_cells(
            self,
            start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        adjacent_cells = self._get_adjacent_cells(start, end)
        for cell in adjacent_cells:
            if cell in self.field:
                return True
        return False

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    if ship.is_drowned:
                        print("x", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
