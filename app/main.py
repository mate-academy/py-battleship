class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (f"Deck ({self.row}, {self.column}) {self.is_alive}")

class Ship:
    def __init__(self, start, end, is_drowned=False):
                self.decks = [
                    Deck(row, column)
                    for row in range(start[0], end[0] + 1)
                    for column in range(start[1], end[1] + 1)
                ]
                self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
            if any(deck.is_alive for deck in self.decks):
                print("Hit!")
            else:
                self.is_drowned = True
                print("Sunk!")
        else:
            print("Miss!")


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

# ship = Ship((0,0), (0,2))
# print(ship.decks)
# ship.fire(0, 0)
# print(ship.is_drowned)
# ship.fire(0, 2)
# print(ship.is_drowned)
# ship.fire(0, 1)
# print(ship.decks)
# print(ship.is_drowned)