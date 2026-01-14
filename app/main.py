class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        """Create decks and save them to a list `self.decks`"""
        self.is_drowned = is_drowned
        self.decks = []

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row, column):
        """Find the corresponding deck in the list"""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        """Change the `is_alive` status of the deck
        And update the `is_drowned` value if it's needed"""

        self.get_deck(row, column).is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                return

        self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        """Create a dict `self.field`.
        Its keys are tuples - the coordinates of the non-empty cells,
        A value for each cell is a reference to the ship
        which is located in it"""

        self.field = {}

        for ship in ships:
            new_ship = Ship(ship[0], ship[1])

            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    self.field[(row, column)] = new_ship

        self._validate_field()

    def fire(self, location: tuple):
        """This function should check whether the location
        is a key in the `self.field`
        If it is, then it should check if this cell is the last alive
        in the ship or not."""

        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self):
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]

                    if ship.is_drowned:
                        print("\033[91m" + u"\u26F5" + "\033[0m", end="\t")
                    elif ship.get_deck(row, column).is_alive:
                        print("\033[92m" + u"\u26F5" + "\033[0m", end="\t")
                    else:
                        print("\033[93m" + u"\u26F5" + "\033[0m", end="\t")

                else:
                    print("~", end="\t")
            print("")

    def _validate_field(self):
        decks_number = [len(deck.__dict__["decks"])
                        for deck in set(self.field.values())]

        if len(decks_number) != 10:
            raise Exception("The total number of the ships should be 10")

        if decks_number.count(1) != 4:
            raise Exception("There should be 4 single-deck ships")

        if decks_number.count(2) != 3:
            raise Exception("There should be 3 double-deck ships")

        if decks_number.count(3) != 2:
            raise Exception("There should be 2 three-deck ships")

        if decks_number.count(4) != 1:
            raise Exception("There should be 1 four-deck ship")

        for coords, ship in self.field.items():
            for row in range(coords[0] - 1, coords[0] + 2):
                for column in range(coords[1] - 1, coords[1] + 2):
                    if (row, column) in self.field \
                            and self.field[(row, column)] != ship:
                        raise Exception(f"Border overlap {coords}")
