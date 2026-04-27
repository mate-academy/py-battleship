class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self):
        return f"Deck({self.row}, {self.column}, {self.is_alive})"

class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.size = None
        self.decks = None
        self.type = None


    def calculate_size_and_type(self):
        self.size = 0
        self.decks = {}


        if self.start == self.end:
            self.size = 1
            self.type = "1-deck"
            self.decks[0] = Deck(row=self.start, column=self.end)


        elif self.start[0] == self.end[0]:
            self.type = "horizontal"
            for current_el in (range(self.start[1], self.end[1] + 1)):
                self.decks[(self.start[0], current_el)] = Deck(row=self.start[0], column=current_el)
                self.size += 1


        elif self.start[1] == self.end[1]:
            self.type = "vertical"

            for  current_el in range(self.start[0], self.end[0] + 1):
                self.decks[(current_el, self.end[0])] = Deck(row=current_el, column=self.end[0])
                self.size += 1


    def get_deck(self, row, column):
        return self.decks[(row, column)]

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False


    def check_is_drowned(self):
        for el in self.decks.values():
            if el.is_alive:
                return False
        return True


ship = Ship(
    (2, 3), (2, 6)
)
ship.calculate_size_and_type()
print(ship.type, ship.size, ship.start, ship.end, ship.is_drowned)
print(ship.decks)
ship.fire(2, 3)
ship.fire(2, 5)
ship.fire(2, 6)
print(ship.check_is_drowned())
print(ship.decks, ship.is_drowned)

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
