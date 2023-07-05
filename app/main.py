"""
~  empty
□ alive
* injured
x drowned
"""


class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False) -> None:  # every single Ship
        self.start = start
        self.end = end

        self.direction = None
        self.get_axis()

        self.decks = []  # all coordinates

        if self.direction == "origin":  # +
            print(self.start, self.end, "ORIGIN")
            self.decks.append(self.start)
            print(self.decks)
        if self.direction == "x":  # +
            print(self.start, self.end, "X")
            self.decks = [(self.start[0], i) for i in range(self.start[1], self.end[1] + 1)]
            print(self.decks)

        if self.direction == "y":  # +
            print(self.start, self.end, "Y")
            self.decks = [(i, self.start[1]) for i in range(self.start[0], self.end[0] + 1)]
            print(self.decks)

    def get_axis(self):
        if self.start == self.end:
            self.direction = "origin"  # □
            return
        if self.start[0] == self.end[0]:
            self.direction = "x"  # □ □ □
            return
        self.direction = "y"    # □
                                # □
                                # □

    def get_deck(self, row: int, column: int) -> None:
        # Find the corresponding deck in the list
        pass

    def fire(self, row: int, column: int) -> None:
        self.is_drowned: bool = not self.is_drowned
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass

    def __str__(self):
        return f"{self.decks}"


class Battleship:
    def __init__(self, ships: list[tuple]):  # Whole game
        for i in ships:
            Ship(start=i[0], end=i[1])
        self.field: dict[tuple(tuple, tuple), Ship] = {}  # Create a dict `self.field`.

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


battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)
