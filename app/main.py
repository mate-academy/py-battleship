class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: list[int],
                 end: list[int],
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`

        self.is_drowned = is_drowned
        self.decks = []

        if start[0] != end[0] and start[1] != end[1]:
            raise ValueError(
                "the ship can be positioned vertically or horizontally")

        if (not (0 <= start[0] < 10)
                or not (0 <= start[1] < 10)
                or not (0 <= end[0] < 10)
                or not (0 <= end[1] < 10)):
            raise ValueError("This ship is not a spaceship. "
                             "It can be positioned on the map")

        if start[0] > end[0] or start[1] > end[1]:
            start, end = end, start

        index = 1 if start[0] == end[0] else 0

        for coord in range(start[index], end[index] + 1):
            coord_x = coord
            coord_y = start[1 - index]
            if index:
                coord_x, coord_y = coord_y, coord_x
            self.decks.append(Deck(coord_x, coord_y))
        if len(self.decks) > 4:
            raise ValueError("the ship can have at most 4 decks")
        self.start = (start[0], start[1])
        self.end = (end[0], end[1])

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

        self.field = {}
        for ship in ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = deck

    def _get_simbol(self, row: int, column: int) -> str:
        simbol = self.field.get((row, column), "~")
        if simbol != "~":
            return u"\u25A1" if simbol.is_alive else "x"
        return simbol

    def fire(self, location: tuple) -> None:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for column in range(10):
                row_str += self._get_simbol(row, column) + "   "
            print(row_str)

#
# ship1 = Ship([8, 3], [5, 3])
# ship2 = Ship([1, 3], [1, 5])
# ships = [ship1, ship2]
# for deck in ship2.decks:
#     print(deck.row, deck.column)
#
# bs = Battleship(ships)
# bs.print_field()
# print(bs.field)
#
