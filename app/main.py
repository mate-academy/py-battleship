import itertools


class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        self.decks = [
            Deck(row, column)
            for row in range(min(start_row, end_row),
                             max(start_row, end_row) + 1)
            for column in range(min(start_column, end_column),
                                max(start_column, end_column) + 1)
        ]

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
        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row, column = location
        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = []
            for column in range(10):
                if (row, column) not in self.field:
                    line.append("~")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        line.append(u"\u25A1")
                    elif ship.is_drowned:
                        line.append("x")
                    else:
                        line.append("*")
            print("\t".join(line))

    def _validate_field(self) -> None:
        ships = {ship for ship in self.field.values()}

        if len(ships) != 10:
            raise ValueError("Total number of the ships should be 10")

        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in ships:
            size = len(ship.decks)
            if size not in counts:
                raise ValueError(f"Invalid ship size: {size}")
            counts[size] += 1

        expected = {1: 4, 2: 3, 3: 2, 4: 1}
        if counts != expected:
            raise ValueError(
                "Should be 4 single-deck, 3 double-deck, "
                "2 three-deck and 1 four-deck ships"
            )

        for (row, column), ship in self.field.items():
            for d_row, d_column in itertools.product((-1, 0, 1), repeat=2):
                if d_row == 0 and d_column == 0:
                    continue
                neighbor = (row + d_row, column + d_column)
                if neighbor in self.field and self.field[neighbor] is not ship:
                    raise ValueError(
                        "Ships shouldn't be located in neighboring cells"
                    )
