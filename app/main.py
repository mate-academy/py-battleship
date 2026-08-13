class Deck:
    def __init__(self, row: int, column: int, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive



class Ship:
    def __init__(self, start: Deck, end: Deck, is_drowned=False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start.row == end.row:
            for column in range(start.column, end.column + 1):
                self.decks.append(Deck(start.row, column))
        elif start.column == end.column:
            for row in range(start.row, end.row + 1):
                self.decks.append(Deck(row, start.column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False



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
