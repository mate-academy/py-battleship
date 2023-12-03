class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def create_decks_between_points(self, start: tuple, end: tuple) -> None:
        for i in range((end[0] - start[0]) + (end[1] - start[1]) + 1):
            if start[0] == end[0]:
                self.decks.append(Deck(start[0], start[1] + i))
            elif start[1] == end[1]:
                self.decks.append(Deck(start[0] + i, start[1]))

    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks_between_points(start, end)

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:

    def create_field(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])

    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.create_field(ships)

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for key in self.field.keys():
            if (key[0][0] <= location[0] <= key[1][0]
                    and key[0][1] <= location[1] <= key[1][1]):
                self.field[key].fire(location[0], location[1])
                if self.field[key].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
