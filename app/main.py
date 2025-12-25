class VisibilityError(Exception):
    def __init__(self) -> None:
        self.message = "The ship isn't field's area"
        super().__init__(self.message)


class LocationError(Exception):
    def __init__(self) -> None:
        self.message = ("Ships shouldn't be located in the "
                        "neighboring cells (even if cells "
                        "are neighbors by diagonal)")
        super().__init__(self.message)


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
            symbol: str = "\u25A1"
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.symbol = symbol

    def __repr__(self) -> str:
        return str(self.__dict__)


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False,
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        """
        This method searches for a deck by coordinate
        :param row:
        :param column:
        :return:
        """
        decks = self.decks
        for deck in decks:
            if deck.row == row and deck.column == column:
                self.fire(row, column)
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        """
        This method exchanges state decks or ships
        :param row:
        :param column:
        :return:
        """
        decks = self.decks
        for deck in decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                deck.symbol = "*"
        decks_values = [deck.is_alive for deck in self.decks]
        if not any(decks_values):
            self.is_drowned = True
            for deck in self.decks:
                deck.symbol = "x"

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list[Deck]:
        """
        This metod creates ship's decks
        :param start:
        :param end:
        :return:
        """
        result = []
        row_start = start[0]
        row_end = end[0]
        column_start = start[1]
        column_end = end[1]
        if start == end:
            result.append(Deck(row_start, column_start))
            return result
        if row_start == row_end:
            for i in range(column_start, column_end + 1):
                result.append(Deck(row_start, i))
        if column_start == column_end:
            for i in range(row_start, row_end + 1):
                result.append(Deck(i, column_start))
        return result

    def __repr__(self) -> str:
        return str(self.__dict__)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = {coords: Ship(coords[0], coords[1]) for coords in ships}
        self.field = [
            (row, column)
            for row in range(10)
            for column in range(10)
        ]
        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        """
        This method fires at the ship for transmitted location
        :param location:
        :return:
        """

        current_ship = None

        for ship in self.ships.values():
            if ship.is_drowned:
                continue
            deck = ship.get_deck(location[0], location[1])
            if deck:
                current_ship = ship

        if not current_ship:
            return "Miss!"
        if any(deck.is_alive for deck in current_ship.decks):
            return "Hit!"
        if not all(deck.is_alive for deck in current_ship.decks):
            return "Sunk!"

    def print_field(self) -> None:
        """
        This method prints all cells of the field line by line.
        :return:
        """
        sea = [["~"] * 10 for i in range(10)]
        decks = sum([ship.decks for ship in self.ships.values()], [])

        for deck in decks:
            row, column = deck.row, deck.column
            sea[row][column] = deck.symbol

        for row in sea:
            print("    ".join(row))

    def _validate_field(self) -> None:
        """
        This method checks ships for their count and their correct placement
        :return:
        """
        coords = self.ships.keys()

        for x_, y_ in coords:
            condition = all((0 <= x_[0] < 10,
                            0 <= x_[1] < 10,
                            0 <= y_[0] < 10,
                            0 <= y_[1] < 10))
            if not condition:
                raise VisibilityError

        assert len(coords) == 10, "The total number of the ships should be 10"

        ships = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        for ship in self.ships.values():
            ships[len(ship.decks)] += 1

        assert ships[1] == 4, "There should be 4 single-deck ships"
        assert ships[2] == 3, "There should be 3 double-deck ships"
        assert ships[3] == 2, "There should be 2 three-deck ships"
        assert ships[4] == 1, "There should be 1 four-deck ship"

        invalid_cells = sum([
            self._get_invalid_cells_for_one_ship(coord)
            for coord in coords
        ], [])

        invalid_cells = set(invalid_cells)
        decks = sum([ship.decks for ship in self.ships.values()], [])
        for cell in invalid_cells:
            for deck in decks:
                if cell[0] == deck.row and cell[1] == deck.column:
                    raise LocationError

    def _get_invalid_cells_for_one_ship(
            self,
            coord: tuple
    ) -> list[tuple]:
        """
        This method find all cells around the ship
        in which other ships can't be located
        :param coord:
        :return:
        """
        row_range = (coord[0][0] - 1, coord[1][0] + 2)
        column_range = (coord[0][1] - 1, coord[1][1] + 2)

        start_row, end_row = row_range
        start_column, end_column = column_range

        current_ship = self.ships[coord].decks

        area_cells = []

        for row in range(start_row, end_row):
            for column in range(start_column, end_column):
                area_cells.append((row, column))

        for deck in current_ship:
            for cell in area_cells:
                if cell[0] == deck.row and cell[1] == deck.column:
                    area_cells.remove(cell)

        return area_cells

    def __repr__(self) -> str:
        return str(self.__dict__)
