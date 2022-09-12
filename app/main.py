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
        self.decks = []

        if self.start[0] == self.end[0]:
            for coord in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], coord))
        if self.start[1] == self.end[1]:
            for coord in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(coord, self.start[1]))
        print(self.decks)

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        try:
            self.get_deck(row, column).is_alive = False
        except AttributeError:
            pass

        if any([deck.is_alive for deck in self.decks]) is False:
            self.is_drowned = True
        return self.is_drowned

class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = {}

        for ship_ in self.ships:

            if ship_[0][0] == ship_[1][0]:

                for coord in range(ship_[0][1], ship_[1][1] + 1):
                    self.field[(ship_[0][0], coord)] = Ship(ship_[0], ship_[1])
            if ship_[0][1] == ship_[1][1]:
                for coord in range(ship_[0][0], ship_[1][0] + 1):
                    self.field[(coord, ship_[0][1])] = Ship(ship_[0], ship_[1])

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        keys_ = []
        keys_ = self.field.keys()

        for key in keys_:
            if key == location:
                self.field[key].fire(location[0], location[1])

                if self.field[key].is_drowned is True:
                    return "Sunk!"

                return "Hit!"
            return "Miss!"


if __name__ == '__main__':
    ships = [
        ((2, 0), (2, 3)),
        ((4, 5), (4, 6)),
        ((3, 8), (3, 9)),
        ((6, 0), (8, 0)),
        ((6, 4), (6, 6)),
        ((6, 8), (6, 9)),
        ((9, 9), (9, 9)),
        ((9, 5), (9, 5)),
        ((9, 3), (9, 3)),
        ((9, 7), (9, 7)),
    ]

    batt = Battleship([
        ((2, 0), (2, 3)),
        ((4, 5), (4, 6)),
        ((3, 8), (3, 9)),
        ((6, 0), (8, 0)),
        ((6, 4), (6, 6)),
        ((6, 8), (6, 9)),
        ((9, 9), (9, 9)),
        ((9, 5), (9, 5)),
        ((9, 3), (9, 3)),
        ((9, 7), (9, 7)),
    ])

    batt.fire((0, 3))
    #batt.fire((1, 7))
    #batt.fire((2, 0))
    #batt.fire((2, 1))
    #batt.fire((2, 2))
    #batt.fire((2, 3))
    #batt.fire((4, 3))
    #batt.fire((4, 5))
