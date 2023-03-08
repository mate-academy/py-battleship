class InvalidFieldError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple[int], end: tuple[int], is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not self.get_status():
            self.is_drowned = True

    def get_status(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return True
        return False

    def __hash__(self) -> int:
        return hash((self.start, self.end))


class Battleship:
    def __init__(self, ships: list[tuple, int]) -> None:
        self.field = {}
        for coordinates in ships:
            start_row, start_column = coordinates[0][0], coordinates[0][1]
            end_row, end_column = coordinates[1][0], coordinates[1][1]
            ship = Ship(coordinates[0], coordinates[1], False)
            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    self.field[(row, column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location[0], location[1]
        if not (row, column) in self.field:
            return "Miss!"
        ship = self.field[(row, column)]
        ship.fire(row, column)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for column in range(0, 10):
                ship = self.field.get((row, column))
                if not ship:
                    print("~    ", end="")
                elif ship.is_drowned:
                    print("x   ", end="")
                elif ship.get_deck(row, column).is_alive:
                    print("□    ", end="")
                else:
                    print("*    ", end="")
            print("")

    def _validate_field(self) -> None:
        ships = {}
        coordinates = []
        for deck, ship in self.field.items():
            if ship not in ships:
                coordinates = []
            coordinates.append(deck)
            ships[ship] = coordinates

        if len(ships.keys()) != 10:
            raise InvalidFieldError("Total number of ships should be 10")

        number_of_decks = [
            len(decks) for decks in ships.values()
        ]
        if not set(number_of_decks).issubset({1, 2, 3, 4}):
            raise InvalidFieldError("A ship should have no more than 4 decks")

        if number_of_decks.count(1) != 4:
            raise InvalidFieldError("There should be 4 single-deck ships")
        if number_of_decks.count(2) != 3:
            raise InvalidFieldError("There should be 3 double-deck ships")
        if number_of_decks.count(3) != 2:
            raise InvalidFieldError("There should be 2 three-deck ships")
        if number_of_decks.count(4) != 1:
            raise InvalidFieldError("There should be 1 four-deck ship")

        for ship, coordinates in ships.items():
            ships_copy = list(ships.values()).copy()
            ships_copy.remove(coordinates)
            ships_copy = [
                coordinate for coordinate_list in ships_copy
                for coordinate in coordinate_list
            ]
            for coordinate in coordinates:
                for row in range(coordinate[0] - 1, coordinate[0] + 2):
                    for column in range(coordinate[1] - 1, coordinate[1] + 2):
                        if (row, column) in ships_copy:
                            raise InvalidFieldError(
                                "Ships shouldn't be located in "
                                "neighboring cells "
                                "(even if cells are neighbors by diagonal)"
                            )
