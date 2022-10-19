class Deck:
    def __init__(self, row, column, is_alive=True):
        self.deck = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.decks = [(Deck(start[0], start[1]))]
        self.is_drowned = is_drowned
        deck_coordinates = list(start)
        while tuple(deck_coordinates) != end:
            if start[1] == end[1]:
                deck_coordinates[0] += 1
                self.decks.append(
                    Deck(deck_coordinates[0], deck_coordinates[1])
                )
            if start[0] == end[0]:
                deck_coordinates[1] += 1
                self.decks.append(
                    Deck(deck_coordinates[0], deck_coordinates[1])
                )

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.deck == (row, column):
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        if self.get_deck(row, column) is not False:
            self.get_deck(row, column).is_alive = False
            alive_decks = 0
            for deck in self.decks:
                if deck.is_alive is True:
                    alive_decks += 1
            if alive_decks == 0:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(start=ship[0], end=ship[1])

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.field.keys():
            decks = [ship[0]]
            start = list(ship[0])
            while tuple(start) != ship[1]:
                if ship[0][1] == ship[1][1]:
                    start[0] += 1
                    decks.append((start[0], start[1]))
                if ship[0][0] == ship[1][0]:
                    start[1] += 1
                    decks.append((start[0], start[1]))
            if location in decks:
                return self.field.get(ship).fire(
                    row=location[0],
                    column=location[1])
        return "Miss!"
