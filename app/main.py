class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        if start[0] == end[0]:
            # horizontal ship
            self.decks = [
                Deck(start[0], x) for x in range(start[1], end[1] + 1)
            ]

        if start[1] == end[1]:
            # vertical ship
            self.decks = [
                Deck(x, start[1]) for x in range(start[0], end[0] + 1)
            ]

        self.is_drowned = is_drowned

        self.life = len(self.decks)

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
            self.life -= 1
            if not self.life:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self):
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    print(self.check_deck_status(row, column), end="   ")
                else:
                    print("~", end="   ")
            print("\n")

    def check_deck_status(self, row, column):
        ship = self.field[row, column]
        if ship.is_drowned:
            return "x"
        if not ship.get_deck(row, column).is_alive:
            return "*"
        return u"\u25A1"

    def _validate_field(self):
        if len(self.ships) != 10:
            print(f"The total number of the ships should be 10, "
                  f"not {len(self.ships)}")
        decks_in_ship = [ship.life for ship in self.ships]
        for i in range(1, 5):
            if decks_in_ship.count(i) != (5 - i):
                print(f"There should be {(5 - i)} {i}-deck ships, "
                      f"not {decks_in_ship.count(i)}")

        # check nearest cells
        for (row, column), ship in self.field.items():
            to_close = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (row + i, column + j) in self.field \
                            and self.field[row + i, column + j] is not ship:
                        to_close = True
            if to_close:
                print("Ships shouldn't be located in the neighboring cells "
                      "(even if cells are neighbors by diagonal)")
