from pprint import pprint


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Deck(start={self.row}, end={self.column})"

    def __repr__(self) -> str:
        return str(self)


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_all_decks()

    def get_deck(self, row: int, column: int) -> None:
        # Find the corresponding deck in the list
        pass

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass

    def get_all_decks(self) -> tuple:
        x_direction = abs(self.start[0] - self.end[0])
        y_direction = abs(self.start[1] - self.end[1])

        if x_direction:
            return [
                Deck(self.start[0] + step, self.start[1])
                for step in range(x_direction + 1)
            ]
        elif y_direction:
            return [
                Deck(self.start[0], self.start[1] + step)
                for step in range(y_direction + 1)
            ]
        else:
            return [Deck(self.start[0], self.start[1])]

    def __str__(self) -> str:
        return f"Ship(start={self.start}, end={self.end})"

    def __repr__(self) -> str:
        return str(self)


class Battleship:
    def __init__(self, ships):
        self.area = [["~"] * 10 for _ in range(10)]
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

        self.make_battle_area()
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

    def make_battle_area(self):
        for ship in self.field.values():
            for deck in ship.decks:
                self.area[deck.row][deck.column] = u"\u25A1"

    def show_area(self):
        for row in self.area:
            print(*row)

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

battle_ship.show_area()
