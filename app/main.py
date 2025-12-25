from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return (f"Deck at position ({self.row}, "
                f"{self.column}), is_alive: {self.is_alive}")


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`

        self.decks = []
        self.is_drowned = is_drowned

        start_deck_row, start_deck_col = start
        end_deck_row, end_deck_col = end

        for row in range(min(start_deck_row, end_deck_row),
                         max(start_deck_row, end_deck_row) + 1):
            for col in range(min(start_deck_col, end_deck_col),
                             max(start_deck_col, end_deck_col) + 1):
                deck = Deck(row, col)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Any | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)

        if deck:
            deck.is_alive = False

            all_dead = True
            for d_k in self.decks:
                if d_k.is_alive:
                    all_dead = False
                    break

            if all_dead:
                self.is_drowned = True

            return True
        return False


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

        self.is_misfire = False
        self.field = {}
        self.ships = []
        self.size = 10
        self.misses = set()

        for ship_coord in ships:
            ship = Ship(ship_coord[0], ship_coord[1])
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> bool:
        if len(self.ships) != 10:
            raise ValueError(
                f"Total number of the ships should be 10,"
                f" got {len(self.ships)}")

        ship_sizes = {}
        for ship in self.ships:
            size = len(ship.decks)
            ship_sizes[size] = ship_sizes.get(size, 0) + 1

        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}
        for size, expected_count in expected_counts.items():
            actual_count = ship_sizes.get(size, 0)
            if actual_count != expected_count:
                raise ValueError(
                    f"Expected {expected_count} "
                    f"ships of size {size}, got {actual_count}")

        vertical_ships = set()
        for ship in self.ships:
            if len(ship.decks) > 1:
                columns = set(deck.column for deck in ship.decks)
                if len(columns) == 1:
                    vertical_ships.add(ship)

        for ship1 in self.ships:
            if ship1 in vertical_ships:
                continue

            ship1_coords = set((deck.row, deck.column) for deck in ship1.decks)

            for ship2 in self.ships:
                if ship1 == ship2 or ship2 in vertical_ships:
                    continue

                ship2_coords = set((deck.row,
                                    deck.column) for deck in ship2.decks)

                for r1, c1 in ship1_coords:
                    for r2, c2 in ship2_coords:
                        if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                            raise ValueError(
                                f"Ships cannot "
                                f"be located in neighboring "
                                f"cells: conflict between {(r1, c1)} "
                                f"and {(r2, c2)}")
        return True

    def print_field(self) -> None:
        for row in range(self.size):
            for coll in range(self.size):
                if (row, coll) in self.field:
                    ship = self.field[(row, coll)]
                    deck = ship.get_deck(row, coll)
                    if ship.is_drowned:
                        print("x", end="     ")
                    elif deck and not deck.is_alive:
                        print("*", end="     ")
                    else:
                        print(u"\u25A1", end="     ")
                elif (row, coll) in self.misses:
                    print("@", end="     ")
                else:
                    print("~", end="     ")
            print("")

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        row, coll = location

        if location in self.field:
            ship = self.field[location]
            ship.fire(row, coll)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        else:
            self.misses.add(location)
            return "Miss!"
