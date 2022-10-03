class Deck:
    def __init__(self, row, column, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_ship()

    def create_ship(self) -> None:
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.end[0], self.end[1]))
        elif self.start[0] == self.end[0]:
            for coords in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], coords))
        elif self.start[1] == self.end[1]:
            for coords in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(coords, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        self.check_if_drowned()

    def check_if_drowned(self) -> None:
        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False
                return
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = dict()
        self.place_ships()

    def place_ships(self) -> None:
        for ship in self.ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            field = []
            for col in range(10):
                if (row, col) not in self.field:
                    field.append(" ~ ")
                else:
                    if self.field[(row, col)].is_drowned:
                        field.append(" x ")
                        continue
                    for deck in self.field[(row, col)].decks:
                        if deck.row == row and deck.column == col:
                            if not deck.is_alive:
                                field.append(" * ")
                            else:
                                field.append(" □ ")
            print(*field)
