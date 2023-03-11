class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], end[1]))
        elif start[0] == end[0]:
            for location_deck in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], location_deck))
        elif start[1] == end[1]:
            for location_deck in range(start[0], end[0] + 1):
                self.decks.append(Deck(start[1], location_deck))
        self.is_drowned = is_drowned

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
        for one_deck in self.decks:
            if one_deck.is_alive is True:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for coordinates in ships:
            self.field[coordinates] = Ship(*coordinates)

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        for ship in self.field.values():
            try:
                ship.fire(*location)
            except AttributeError:
                pass
            else:
                if ship.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
