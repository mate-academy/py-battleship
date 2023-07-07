class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        self._create_decks(start, end)

    def _create_decks(self, start: tuple, end: tuple) -> None:
        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(start_row, column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, start_column))

    def get_deck(self, row: tuple, column: tuple) -> tuple:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: tuple, column: tuple) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self._check_drowned()

    def _check_drowned(self) -> None:
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self._create_field(ships)

    def _create_field(self, ships: list) -> None:
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    self.field[(row, column)] = new_ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def create_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for location, ship in self.field.items():
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = u"\u25A1"
                else:
                    field[deck.row][deck.column] = "x"
        for row in field:
            print(" ".join(row))
