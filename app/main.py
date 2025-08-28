class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
            the_ship: None | object = None) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.the_ship = the_ship if the_ship is not None else None


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck
        raise ValueError(
            f"No such deck with coordinates: row {row}, column {column}")

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        target = self.get_deck(row, column)
        target.is_alive = False
        self.hitpoints -= 1
        if self.hitpoints == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.deployed_ships = []
        self.battlefield = []
        self._validate_field(ships)
        self.ships_to_field(ships)
        self.check_ship_types()
        self.check_adjustments()
        self.set_battlefield()
        self.deploy_ships()

    def default_fields_restore(
            self,
            error_text: str = "Incorrect input when field is established!"
    ) -> None:
        self.field = {}
        self.deployed_ships = []
        self.battlefield = []
        raise ValueError(error_text)

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        row, column = location
        if location in self.field:
            if not self.field[location].is_alive:
                raise ValueError(
                    "It is forbidden to shot shame spot more, than once!"
                )
            ship = self.field[location].the_ship
            ship.fire(row, column)
            if not ship.is_drowned:
                self.battlefield[row][column] = "*"
                return "Hit!"
            else:
                for deck in ship.decks:
                    self.battlefield[deck.row][deck.column] = "x"
                return "Sunk!"
        self.battlefield[row][column] = "o"
        return "Miss!"

    def ships_to_field(self, ships: list) -> None:
        for ship in ships:
            start, end = ship
            new_ship = Ship(ship[0], ship[1])
            # If the ship is placed horizontally - axis = 1, vertically - 0
            axis = 0 if start[0] != end[0] else 1
            for deck in range(start[axis], end[axis] + 1):
                if axis:
                    new_deck = Deck(start[0], deck, the_ship=new_ship)
                else:
                    new_deck = Deck(deck, start[1], the_ship=new_ship)
                # Prevents multiple placements in the same spot
                if (new_deck.row, new_deck.column) in self.field:
                    self.default_fields_restore(
                        "No deck might be placed more than once!")
                new_ship.decks.append(new_deck)
                self.field[new_deck.row, new_deck.column] = new_deck
            new_ship.hitpoints = len(new_ship.decks)
            self.deployed_ships.append(new_ship)

    def set_battlefield(self) -> None:
        for row in range(10):
            self.battlefield.append([])
            for _ in range(10):
                self.battlefield[row].append("~")

    def deploy_ships(self) -> None:
        for ship in self.deployed_ships:
            for deck in ship.decks:
                self.battlefield[deck.row][deck.column] = u"\u25A1"

    def print_field(self) -> None:
        to_print = self.battlefield.copy()
        to_print = "\n".join(["".join(row) for row in to_print])
        print(to_print)

    def check_ship_types(self) -> None:
        # Checks if there are exactly that many ships with that many decks,
        # as it should be
        self.deployed_ships.sort(key=lambda ship: ship.hitpoints)
        expected_occurences = 4
        occurence = 0
        decks = 1
        for ship in self.deployed_ships:
            if ship.hitpoints == decks:
                occurence += 1
            else:
                self.default_fields_restore()
            if occurence == expected_occurences:
                expected_occurences -= 1
                occurence = 0
                decks += 1

    def check_adjustments(self) -> None:
        # Checks if no ships are located next to each other
        occupied = []
        for ship in self.deployed_ships:
            for deck in ship.decks:
                pos = (deck.row, deck.column)
                for diag_row in [-1, 0, 1]:
                    for diag_col in [-1, 0, 1]:
                        neighbor = (pos[0] + diag_row, pos[1] + diag_col)
                        if neighbor in occupied:
                            self.default_fields_restore(
                                "No ships might be next to each other!")
                        else:
                            occupied.append(neighbor)

    def _validate_field(self, ships: list) -> None:
        for ship in ships:
            # Checks, if no coordinate is beyond boundaries:
            for coordinate in ship:
                for dot in coordinate:
                    if dot < 0 or dot > 9:
                        self.default_fields_restore(
                            "No coordinate beyond boundaries!")
            start, end = ship
            # Checks if every ship is strictly horizontal or vertical
            if start[0] != end[0] and start[1] != end[1]:
                self.default_fields_restore(
                    "Every ship must be strictly horizontal or vertical!")


if __name__ == "__main__":
    pass
