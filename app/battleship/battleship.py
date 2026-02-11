class Battleship:
    def __init__(self, ships, field):
        self.ships = ships
        self.field = field
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for (x1, y1), (x2, y2) in self.ships:

            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    field[x1][y] = u"\u25A1"

            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    field[x][y1] = u"\u25A1"


    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def print_field(self):
        for row in self.field:
            print(" ".join(row))