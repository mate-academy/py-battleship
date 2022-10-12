class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:

        self.decks = {(i, j): Deck(i, j)
                      for i in range(start[0], end[0] + 1)
                      for j in range(start[1], end[1] + 1)}
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive
                   for deck in self.decks.values()):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.ships = [Ship(x, y) for x, y in ships]
        self.field = {}
        self.field.update({deck: ship
                           for ship in self.ships
                           for deck in ship.decks.keys()})
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

    def fire(self, location: tuple[int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if not self.field.get(location):
            return "Miss!"

        return self.field[location].fire(*location)
