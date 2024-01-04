class Deck:
    def __init__(self, row, column, is_alive=True) -> None:
        self.field = (row, column)
        self.is_alive = is_alive

    def change_is_alive(self):
        if self.is_alive:
            self.is_alive = False


class Ship:
    def __init__(self, start, end, is_drowned=False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.decks.append(Deck(start, end))
        self.is_drowned = is_drowned

    def get_deck(self, row, column) -> Deck | bool:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.field == (row, column):
                return deck
        return False

    def fire(self, row, column) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)

        if deck:
            deck.change_is_alive()

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass
