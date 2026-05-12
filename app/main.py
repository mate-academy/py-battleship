class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            ship: Ship,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.ship = ship


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`

        self.is_drowned = is_drowned
        self.decks = []

        if start[0] != end[0] and start[1] != end[1]:
            raise ValueError(
                "the ship can be positioned vertically or horizontally")

        if (not (0 <= start[0] < 10)
                or not (0 <= start[1] < 10)
                or not (0 <= end[0] < 10)
                or not (0 <= end[1] < 10)):
            raise ValueError("This ship is not a spaceship. "
                             "It can be positioned on the map 10 x 10")

        if start[0] > end[0] or start[1] > end[1]:
            start, end = end, start

        index = 1 if start[0] == end[0] else 0

        for coord in range(start[index], end[index] + 1):
            coord_x = coord
            coord_y = start[1 - index]
            if index:
                coord_x, coord_y = coord_y, coord_x
            self.decks.append(Deck(coord_x, coord_y, self))
        if len(self.decks) > 4:
            raise ValueError("the ship can have at most 4 decks")
        self.start = (start[0], start[1])
        self.end = (end[0], end[1])

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if any(deck.is_alive for deck in self.decks):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

        self.field = {}
        for coord in ships:
            ship = Ship(coord[0], coord[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = deck

        self._validate_field()

    def _get_simbol(self, row: int, column: int) -> str:
        simbol = self.field.get((row, column), "~")
        if simbol != "~":
            return u"\u25A1" if simbol.is_alive else \
                "x" if simbol.ship.is_drowned else "*"
        return simbol

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        deck = self.field.get(location, None)
        if deck is None:
            return "Miss!"
        return deck.ship.fire(*location)

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for column in range(10):
                row_str += self._get_simbol(row, column) + "   "
            print(row_str)

    def _validate_field(self) -> bool:
        ships = {cell.ship for cell in self.field.values()}

        if len(ships) != 10:
            print(f"There should be 10 ships, but now there are {len(ships)}")
            return False

        ships_count = {}
        for ship in ships:
            size = len(ship.decks)
            ships_count[size] = ships_count.get(size, 0) + 1

        str_dict = {1: "single", 2: "double", 3: "three", 4: "four"}
        for index in range(1, 5):
            if ships_count[index] != 5 - index:
                print(f"Wrong number of {str_dict[index]}-deck ships. "
                      f"Should be {5 - index}.")
                return False

        for ship in ships:
            start_row, start_column = ship.start
            end_row, end_column = ship.end
            start_row -= 1 if start_row > 0 else 0
            start_column -= 1 if start_column > 0 else 0
            end_row += 1 if end_row < 9 else 0
            end_column += 1 if end_column < 9 else 0

            for index_row in range(start_row, end_row + 1):
                for index_column in range(start_column, end_column + 1):
                    own_ship = False
                    for deck in ship.decks:
                        if (index_row == deck.row
                                and index_column == deck.column):
                            own_ship = True
                            break
                    if not own_ship:
                        if self._get_simbol(index_row, index_column) != "~":
                            print(f"Placement error near point "
                                  f"{index_row} : {index_column}")
                            return False

        return True
