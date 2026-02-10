class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        pass

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships, field):
        self.ships = ships
        self.field = field
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for point in ships:
            # self.field[point[0]] = "lol"
            # self.field[point[1]] = "kek"
            print(self.field[0][2])




    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def print_field(self):
        for row in self.field:
            print(" ".join(row))


field = [["~"] * 10 for _ in range(10)]

ships = [
    ((0, 0), (0, 3))
]

battle_ship = Battleship(ships, field)

battle_ship.print_field()
