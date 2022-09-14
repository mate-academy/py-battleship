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

    def create(self):

        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
            return self.decks
        if self.start[0] == self.end[0]:
            for coord in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], coord))
        if self.start[1] == self.end[1]:
            for coord in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(coord, self.start[1]))

        return self.decks

    def get_deck(self, row, column):
        #Find the corresponding deck in the list

        for deck in self.decks:
            if deck.row == row and deck.column == column:

                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.create()

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                try:
                    self.get_deck(deck.row, deck.column).is_alive = False
                    deck.is_alive = False

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

            if ship_[0][0] == ship_[1][0] and ship_[0][1] == ship_[1][1]:
                self.field[(ship_[0])] = Ship(ship_[0], ship_[1])

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

        for key, value in self.field.items():

            if key[0] == location[0] and key[1] == location[1]:

                self.field[key].fire(location[0], location[1])
                #print(key, self.field[key].is_drowned, location)
                if self.field[key].is_drowned is True:
                    return "Sunk!"

                return "Hit!"
        return "Miss!"


if __name__ == '__main__':
    battle_ship = Battleship(
        [
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
    )
    battle_ship.fire((0, 4))
    battle_ship.fire((1, 7))
    battle_ship.fire((2, 0))
    battle_ship.fire((2, 1))
    battle_ship.fire((2, 2))
    battle_ship.fire((2, 3))
    #battle_ship.fire((4, 3))
    #battle_ship.fire((4, 5))
    #battle_ship.fire((5, 5))
    #battle_ship.fire((4, 6))
    #battle_ship.fire((9, 5))
    #battle_ship.fire((9, 6))
    #battle_ship.fire((9, 5))
