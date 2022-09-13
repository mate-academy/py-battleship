class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    total_number_of_ships = 0
    type_of_ships = {"1_decks": 0,
                     "2_decks": 0,
                     "3_decks": 0,
                     "4_decks": 0}

    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_ship()

    # Create decks and save them to a list `self.decks`
    def create_ship(self):
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))
        if self.start[0] != self.end[0]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))
        if self.start[1] != self.end[1]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        Ship.total_number_of_ships += 1
        Ship.type_of_ships[f"{len(self.decks)}_decks"] += 1

    # Find the corresponding deck in the list
    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    # Change the `is_alive` status of the deck
    # And update the `is_drowned` value if it's needed
    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        # Create a dict `self.field`.
        self.field = {}

        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        # Check the following conditions after creating a field
        self._validate_field()

    # This function should check whether the location
    # is a key in the `self.field`
    # If it is, then it should check if this cell is the last alive
    # in the ship or not.
    def fire(self, location: tuple):
        if location in self.field.keys():
            value = self.field[location]
            return value.fire(location[0], location[1])
        return "Miss!"

    def print_field(self):
        field = []
        for _ in range(10):
            field.append(["~"] * 10)

        for point_of_ship in self.field.keys():
            ship = self.field[point_of_ship]
            deck_status = ship.get_deck(point_of_ship[0], point_of_ship[1])
            if ship.is_drowned is True:
                field[point_of_ship[0]][point_of_ship[1]] = "X"
            if deck_status.is_alive is False:
                field[point_of_ship[0]][point_of_ship[1]] = "*"
            else:
                field[point_of_ship[0]][point_of_ship[1]] = "\u25A1"

        for line in field:
            print(line)

    @staticmethod
    def _validate_field():
        if Ship.total_number_of_ships != 10:
            raise ValueError("Ships should be 10")
        if Ship.type_of_ships["1_decks"] != 4:
            raise ValueError("Single-deck ships should be 4")
        if Ship.type_of_ships["2_decks"] != 3:
            raise ValueError("Double-deck ships should be 3")
        if Ship.type_of_ships["3_decks"] != 2:
            raise ValueError("Three-deck ships ships should be 2")
        if Ship.type_of_ships["4_decks"] != 1:
            raise ValueError("Four-deck ship ships should be 1")
