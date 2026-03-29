class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.field = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        self.decks.append(Deck(*start))

        if start_row == end_row:
            current_column = start_column

            while current_column != end_column:
                current_column += 1
                self.decks.append(Deck(start_row, current_column))

        if start_column == end_column:
            current_row = start_row

            while current_row != end_row:
                current_row += 1
                self.decks.append(Deck(current_row, start_column))

    def get_deck(
        self,
        row: int,
        column: int
    ) -> Deck | bool:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.field == (row, column):
                return deck
        return False

    def fire(
        self,
        row: int,
        column: int
    ) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)

        if deck and self.is_drowned is False:
            deck.is_alive = False
            if all(
                deck.is_alive is False for deck in self.decks
            ):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}

        for coordinates in ships:
            ship = Ship(*coordinates)
            self._validate_field(ship)
            self.field.update(
                {deck.field: ship for deck in ship.decks}
            )

    def _validate_field(self, ship: Ship) -> None:
        self._ships_amount = 0
        self._one_board_ships = 0
        self._two_board_ships = 0
        self._three_board_ships = 0
        self._four_board_ships = 0

        for deck in ship.decks:
            ship_row, ship_column = deck.field
            for field in self. field:
                field_row, field_column = field
                if (
                    ship_row == field_row
                    or ship_row + 1 == field_row
                    or ship_row == field_row + 1
                ) and (
                    ship_column == field_column
                    or ship_column + 1 == field_column
                    or ship_column == field_column + 1
                ):
                    raise AssertionError("Ships can't contact")

        if self._ships_amount == 10:
            raise AssertionError("Not more then 10 ships")

        if len(ship.decks) == 1:
            if self._one_board_ships == 4:
                raise AssertionError("Not more then 4 one_board ships")
            else:
                self._one_board_ships += 1

        if len(ship.decks) == 2:
            if self._two_board_ships == 3:
                raise AssertionError("Not more then 3 two_board ships")
            else:
                self._two_board_ships += 1

        if len(ship.decks) == 3:
            if self._three_board_ships == 2:
                raise AssertionError("Not more then 2 three_board ships")
            else:
                self._three_board_ships += 1

        if len(ship.decks) == 4:
            if self._four_board_ships == 1:
                raise AssertionError("Not more then 1 four_board ships")
            else:
                self._four_board_ships += 1

        self._ships_amount += 1

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            return self.field[location].fire(*location)
        else:
            return "Miss!"
