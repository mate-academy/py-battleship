class InvalidFieldError(ValueError):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        elif start[1] == end[1]:
            self.decks = [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]
        else:
            self.decks = []

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        current_deck = self.get_deck(row, column)
        if current_deck is not None:
            current_deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.field.update({
                (deck.row, deck.column): ship
                for deck in ship.decks
            })

        self._validate_field()

    def _validate_field(self) -> None:
        # Validate number/types of ships
        unique_ships = set(self.field.values())
        if len(unique_ships) != 10:
            raise InvalidFieldError("The total number of the ships "
                                    "should be 10")
        ships_counter = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in unique_ships:
            ships_counter[len(ship.decks)] += 1
        correct_ship_counter = {1: 4, 2: 3, 3: 2, 4: 1}
        for decks, value in ships_counter.items():
            if value != correct_ship_counter[decks]:
                raise InvalidFieldError(f"there should be "
                                        f"{correct_ship_counter[decks]} "
                                        f"{decks}-deck ships")

        # Validate ship positions
        for (current_row, current_column) in self.field:
            for row in range(current_row - 1, current_row + 2):
                for column in range(current_column - 1, current_column + 2):
                    if ((row, column) in self.field and (row, column)
                            != (current_row, current_column)):
                        if (self.field[(current_row, current_column)]
                                != self.field[(row, column)]):
                            raise InvalidFieldError("Ships shouldn't be "
                                                    "located in the "
                                                    "neighboring cells "
                                                    "(even if cells are "
                                                    "neighbors by "
                                                    "diagonal).")

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location)
        if not ship:
            return "Miss!"

        ship.fire(*location)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""

            for column in range(10):
                ship = self.field.get((row, column))

                if ship is None:
                    line += "~    "
                    continue

                if ship.is_drowned:
                    line += "x   "
                    continue

                deck = ship.get_deck(row, column)
                if deck.is_alive:
                    line += u"\u25A1    "
                else:
                    line += "*    "

            print(line)
