class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return (f"Deck - row:{self.row},"
                f" column:{self.column}, is_alive:{self.is_alive}")


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
        else:
            raise AttributeError("Deck is not exist")

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list[Deck]:
        x1, y1 = start
        x2, y2 = end
        start_deck = Deck(row=x1, column=y1)
        decks = [start_deck]
        while (x1, y1) != (x2, y2):
            if x1 != x2:
                x1 += 1
            if y1 != y2:
                y1 += 1
            decks.append(Deck(row=x1, column=y1))
        return decks


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [
            Ship(*self.sort_ship_by_direction(ship))
            for ship in ships
        ]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location, None)
        if ship is None:
            return "Miss!"

        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10")
        expected_types = {1: 4, 2: 3, 3: 2, 4: 1}
        counts = {}
        for ship in self.ships:
            length = len(ship.decks)
            counts[length] = counts.get(length, 0) + 1

        for length, needed in expected_types.items():
            actual = counts.get(length, 0)
            if actual != needed:
                raise ValueError(f"Expected {needed} "
                                 f"ships of length "
                                 f"{length}, got {actual}")

        for ship in self.ships:
            for deck in ship.decks:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = deck.row + dr, deck.column + dc
                        if 0 <= nr < 10 and 0 <= nc < 10:
                            other = self.field.get((nr, nc))
                            if other is not None and other is not ship:
                                raise ValueError(f"Ships "
                                                 f"are adjacent at {(nr, nc)}"
                                                 f" and "
                                                 f"{(deck.row, deck.column)}")

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                deck_owner = self.field.get((row, col))
                print_value = "~"
                if deck_owner is None:
                    print_value = print_value
                else:
                    deck = deck_owner.get_deck(row, col)
                    if deck.is_alive:
                        print_value = "□"
                    elif deck_owner.is_drowned:
                        print_value = "x"
                    else:
                        print_value = "*"
                print(print_value, end=" ")
            print()

    @staticmethod
    def sort_ship_by_direction(ship: tuple) -> list:
        if ship[0][0] == ship[1][0]:
            return sorted(ship, key=lambda e: e[1])
        return sorted(ship, key=lambda e: e[0])

    def __repr__(self) -> str:
        return f"field: {self.field}, ships: {self.ships}"
