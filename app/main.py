from collections import Counter


class Deck:
    def __init__(self,
                 row: int,
                 col: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.col = col
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        row1, col1 = start
        row2, col2 = end

        if row1 == row2:
            for col in range(col1, col2 + 1):
                self.decks.append(Deck(row1, col))
        elif col1 == col2:
            for row in range(row1, row2 + 1):
                self.decks.append(Deck(row, col1))
        else:
            raise ValueError("Invalid coords for ship")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.col == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    ROWS: int = 10
    COLS: int = 10

    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]],
                 ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        self.ships: list[Ship] = []
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.col)] = ship

        self._validate_input()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            row, col = location
            ship.fire(row, col)

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        for row in range(Battleship.ROWS):
            for col in range(Battleship.COLS):
                location = (row, col)
                if location in self.field:
                    ship = self.field.get(location)
                    if ship.get_deck(row, col).is_alive:
                        print("□", end=" ")
                    elif ship.is_drowned:
                        print("X", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_input(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Number of ships is not valid: should be 10")

        ships_number = Counter([len(ship.decks) for ship in self.ships])
        expected_ships_number = {1: 4, 2: 3, 3: 2, 4: 1}

        for ship, number in expected_ships_number.items():
            actual = ships_number.get(ship, 0)
            if number != actual:
                raise ValueError(f"Invalid number of {ship}-deck ships: "
                                 f"should be {number}, got {actual}")

        for ship in ships_number:
            if ship not in expected_ships_number:
                raise ValueError(f"Invalid ship size: {ship}")

        coords: set[tuple[int, int]] = set()
        for ship in self.ships:
            for deck in ship.decks:
                coord = (deck.row, deck.col)
                if coord in coords:
                    raise ValueError(f"Overlapping ships at {coord}")

                coords.add(coord)

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for (row, col), ship in self.field.items():
            for dr, dc in directions:
                neighbour = row + dr, col + dc

                if neighbour in self.field:
                    neighbour_ship = self.field.get(neighbour)

                    if neighbour_ship != ship:
                        raise ValueError(f"Overlapping ships at {neighbour}")
