class Deck:
    def __init__(self, row, column, is_alive=True):
        self.position = (row, column)
        self.is_alive = is_alive


class Ship:

    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        # Create decks and save them to a list `self.decks`
        if start[0] == end[0]:
            if start[1] == end[1]:
                self.decks.append(Deck(start[0], start[1]))
            else:
                for i in range(end[1] - start[1] + 1):
                    self.decks.append(Deck(start[0], start[1] + i))
        else:
            for i in range(end[0] - start[0] + 1):
                self.decks.append(Deck(start[0] + i, start[1]))

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    ships_dict = {}

    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for ship in ships:
            self.ships_dict[ship] = Ship(ship[0], end=ship[1])
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in Battleship.ships_dict.values():
            for deck in ship.decks:
                if deck.position == location:
                    deck.is_alive = False
                    for deck_ in ship.decks:
                        if deck_.is_alive:
                            return "Hit!"
                    return "Sunk!"
        else:
            return "Miss!"
