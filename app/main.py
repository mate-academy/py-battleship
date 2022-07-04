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
                        print(u"\u2620", end="\t")
                    elif ship.get_deck(row, column).is_alive:
                        print(u"\u26F5", end="\t")
                    else:
                        print(u"\u2622", end="\t")

                else:
                    print("~", end="\t")
            print("")
