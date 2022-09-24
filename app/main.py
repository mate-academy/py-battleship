class WrongCoordinates(Exception):
    pass


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for decks in self.decks:
            if decks.is_alive:
                break
        else:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    self.field[(row, column)] = new_ship
        if not self._validate_field():
            raise WrongCoordinates("Ships located in the neighboring cells")

    def fire(self, location: tuple):
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

    def print_field(self):
        for i in range(10):
            for j in range(10):
                if (i, j) in self.field:
                    deck = self.field[i, j].get_deck(i, j)
                    if deck.is_alive:
                        print(u"\u25A1", end="\t")
                    else:
                        print("x", end="\t")
                else:
                    print("~", end="\t")
            print()

    def _validate_field(self):
        ship_len = {i: 0 for i in range(1, 5)}
        for location, ship in self.field.items():
            ship_len[len(ship.decks)] += 1
        if ship_len != {i: abs(i - 5) * i for i in range(1, 5)}:
            return False
        all_ship = set(self.field.values())
        for ship in all_ship:
            for i in range(0, -2, -1):
                cell_list = self._list_cell(ship.decks[i].row,
                                            ship.decks[i].column)
                for cell in cell_list:
                    if cell in self.field and ship != self.field[cell]:
                        return False
                if (ship.decks[0].row, ship.decks[0].column) ==\
                        (ship.decks[- 1].row, ship.decks[- 1].column):
                    continue
        return True

    @staticmethod
    def _list_cell(row, column):
        is_empty = [(row + 1, column),
                    (row + 1, column + 1),
                    (row + 1, column - 1),
                    (row, column + 1),
                    (row, column - 1),
                    (row - 1, column),
                    (row - 1, column + 1),
                    (row - 1, column - 1)]
        return is_empty
