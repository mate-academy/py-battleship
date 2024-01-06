class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive=True
    ) -> None:
        self.field = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned=False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        self.decks.append(Deck(*start))

        if start_row == end_row:
            current_column = start_column

            while current_column != end_column:
                current_column += 1
                self.decks.append(Deck(start_row, current_column))

        if start_column == end_column:
            current_row = start_row

            while current_row != end_column:
                current_row += 1
                self.decks.append(Deck(current_row, start_column))


    def get_deck(
        self,
        row: int,
        column: int
    ) -> Deck | bool:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.field == (row, column):
                return deck
        return False

    def fire(
        self,
        row: int,
        column: int
    ) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)

        if deck and self.is_drowned is False:
            deck.is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}


    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass
