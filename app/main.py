from tabulate import tabulate

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
        is_drowned = is_drowned

        self.direction = None
        self.get_axis()

        self.decks = []  # all coordinates step by step

        """."""
        if self.direction == "origin":
            print(self.start, self.end, "ORIGIN")
            self.decks.append(self.start)
            print(self.decks)

        """---->"""
        if self.direction == "x":
            print(self.start, self.end, "X")
            self.decks = [(self.start[0], coord) for coord
                          in range(self.start[1], self.end[1] + 1)]
            print(self.decks)

        """↓"""
        if self.direction == "y":
            print(self.start, self.end, "Y")
            self.decks = [(coord, self.start[1]) for coord
                          in range(self.start[0], self.end[0] + 1)]
            print(self.decks)

    def get_axis(self):
        if self.start == self.end:
            self.direction = "origin"  # □
            return
        if self.start[0] == self.end[0]:
            self.direction = "x"  # □ □ □
            return
        self.direction = "y"  # □
        # ______________________□
        # ______________________□

    def get_deck(self, row: int, column: int) -> tuple:
        for deck in self.decks:
            if deck == (row, column):
                return deck  # why i even need it
        # Find the corresponding deck in the list

    def fire(self, row: int, column: int) -> None:

        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass  # why i even need it

    def __str__(self):
        return f"{self.decks}"


class Battleship:
    def __init__(self, ships: list[tuple]):  # Whole game
        self.field = {}  # Create a dict `self.field`. # ((), (), ... ()) : self.Ship
        print()
        for i in ships:
            ship = Ship(start=i[0], end=i[1])
            for deck in ship.decks:
                print(deck)
                self.field[deck] = ship
        self.validate_input()
        self.print_field()

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def print_field(self):

        self.field = [["~" for column in range(10)] for field in range(10)]
        print(tabulate(self.field, tablefmt="grid"))

    def validate_input(self):
        pass


if __name__ == '__main__':
    print("main")
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
