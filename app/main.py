class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.decks_creation()

    def decks_creation(self):
        decks = []
        for i in range(self.start[0], self.end[0] + 1):
            for j in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(row=i, column=j))
        return decks

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        self.is_drowned = all([deck.is_alive is False for deck in self.decks])
        return self.is_drowned


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = self.field_creation()

    def field_creation(self):
        field = {}
        for ship in self.ships:
            ship_obj = Ship(start=ship[0], end=ship[1])
            decks = ship_obj.decks
            for deck in decks:
                field[(deck.row, deck.column)] = ship_obj
        return field

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"
        elif self.field[location].fire(location[0], location[1]):
            return "Sunk!"
        return "Hit!"
