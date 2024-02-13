class Deck:
    def __init__(self, row, column, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False) -> None:
        self.decks: list = self._get_deck(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def _get_deck(start, end) -> list:
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            return [(x1, y) for y in range(
                min(y1, y2), max(y1, y2) + 1)]
        elif y1 == y2:
            return [(x, y1) for x in range(
                min(x1, x2), max(x1, x2) + 1)]

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    field = [["~" for _ in range(10)] for _ in range(10)]

    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.ships_on_the_field()

    def ships_on_the_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                x1, y1 = deck
                Battleship.field[x1][y1] = u"\u25A1"
                # print(f"{deck}")

    def fire(self: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    @staticmethod
    def print_field() -> None:
        for row in Battleship.field:
            print("  ".join(row))


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
print(battle_ship.print_field())
