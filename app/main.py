class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self._validate_deck()

    def _validate_deck(self) -> None:
        if self.row > 9 or self.column > 9:
            print("The Field has 10 x 10 sells")


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> float:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def check_drown(self) -> bool:
        return all(deck.is_alive is False for deck in self.decks)

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if self.check_drown():
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[deck.row, deck.column] = new_ship
        self._validate_field()

    def _validate_field(self) -> None:

        list_ships = set(self.field.values())
        if len(list_ships) != 10:
            print("Not enough ships!!!Must be 10")
        ships = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in list_ships:
            if len(ship.decks) == 1:
                ships[1] += 1
            if len(ship.decks) == 2:
                ships[2] += 1
            if len(ship.decks) == 3:
                ships[3] += 1
            if len(ship.decks) == 4:
                ships[4] += 1
        if ships[1] != 4:
            print("Single ships must be 4!!!")
        if ships[2] != 3:
            print("Double ships must be 3!!!")
        if ships[3] != 2:
            print("Triple ships must be 2!!!")
        if ships[4] != 1:
            print("Quater ships must be 1!!!")

        for (row, column), shep in self.field.items():
            check_deck = (row, column)
            neighbors = [
                (row - 1, column - 1),
                (row - 1, column),
                (row - 1, column + 1),
                (row, column - 1),
                (row, column + 1),
                (row + 1, column - 1),
                (row + 1, column),
                (row + 1, column + 1),
            ]
            for deck in neighbors:
                if deck in self.field and (
                    self.field[deck] != self.field[check_deck]
                ):
                    print("Ships can't be near each other")

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        return ship.fire(*location)

    def print_field(self) -> None:
        clean_field = [["~" for _ in range(10)] for _ in range(10)]
        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)
            if ship.check_drown():
                clean_field[row][column] = "x"
            elif deck.is_alive is False:
                clean_field[row][column] = "*"
            else:
                clean_field[row][column] = "□"
        for element in clean_field:
            for el in element:
                print(el, end=" ")
            print()
