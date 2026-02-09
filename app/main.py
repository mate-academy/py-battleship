class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column =column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            for row in range(min(start[1], end[1]), max(start[1] + 1, end[1] + 1)):
                self.decks.append(Deck(start[0], row))
        else:
            for column in range(min(start[0], end[0]), max(start[0] + 1, end[0] + 1)):
                self.decks.append(Deck(column, start[1]))


    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if  all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            if ship[0][0] in range(0,10) and ship[0][1] in range(0,10) and ship[1][0] in range(0, 10) and ship[1][1] in range(0, 10):
                tmp_ship_object = Ship(ship[0],ship[1])
                if ship[0][0] == ship[1][0]:
                    for value in range(min(ship[0][1], ship[1][1]), max(ship[0][1] + 1, ship[1][1] + 1)):
                        self.field[(ship[0][0], value)] = tmp_ship_object
                else:
                    for value in range(min(ship[0][0], ship[1][0]), max(ship[0][0] + 1, ship[1][0] + 1)):
                        self.field[(value, ship[0][1])] = tmp_ship_object

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned is False:
                return "Hit!"
            return "Sunk!"
        return "Miss!"
