class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        row_start, column_start = self.start
        row_end, column_end = self.end

        if row_start == row_end:
            while column_start <= column_end:
                self.decks.append(Deck(row_start, column_start))
                column_start += 1

        elif column_start == column_end:
            while row_start <= row_end:
                self.decks.append(Deck(row_start, column_start))
                row_start += 1

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        try:
            fire_deck = self.get_deck(row, column)
            fire_deck.is_alive = False
            if not self.check_if_drowned():
                return "Hit!"
            else:
                self.is_drowned = True
                return "Sunk!"
        except ValueError:
            return "Miss!"

    def check_if_drowned(self) -> bool:
        return not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple[int, int]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

        self.ship_matrix = [["~" for _ in range(10)] for _ in range(10)]
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for deck_coords, ship in self.field.items():
            if location == deck_coords:
                return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        for row, column in self.field.keys():
            ship = self.field[(row, column)]
            deck = ship.get_deck(row, column)
            if deck.is_alive:
                self.ship_matrix[row][column] = u"\u25A1"
            elif not ship.is_drowned:
                self.ship_matrix[row][column] = "*"
            else:
                self.ship_matrix[row][column] = "x"
        for _row in self.ship_matrix:
            print(_row, "\n")

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10")

        ship_decks = sorted(len(ship.decks) for ship in self.ships)
        if ship_decks != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError(
                "There should be 4 single-deck ships;"
                "\nThere should be 3 double-deck ships;"
                "\nThere should be 2 three-deck ships;"
                "\nThere should be 1 four-deck ship;"
            )

        for (row, column), ship in self.field.items():
            row_counters = [-1, 0, 1]
            column_counters = [-1, 0, 1]

            for row_counter in row_counters:
                for column_counter in column_counters:
                    if row_counter == 0 and column_counter == 0:
                        continue
                    close_ship = self.field.get(
                        (
                            row + row_counter, column + column_counter
                        ),
                        None
                    )
                    if close_ship is not None and close_ship is not ship:
                        raise ValueError(
                            "Ships shouldn't be located "
                            "in the neighboring cells "
                            "(even if cells are neighbors by diagonal)"
                        )
