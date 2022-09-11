class Deck:
    def __init__(self, row: int = 9, column: int = 9, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def print_field(self):
        temp_list = ["~"] * self.column
        for i in range(self.column):
            temp_list[i] = ["~"] * self.column
        for i in temp_list:
            print(i)
        print("")


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        # Create decks and save them to a list `self.decks`
        # Find the corresponding deck in the list

    def get_deck(self, row, column):
        list_deck = Deck()
        print(list_deck)

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships):
        self.ships = ships

        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass


deck = Deck()
deck.print_field()

list_of_ships = [
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
list_ships = Battleship(list_of_ships)

