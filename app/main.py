class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks = Deck(start, end)
        if start[0] == end[0]:
            self.decks = [Deck(start[0], end[0] + i)
                          for i in range(abs(start[1] - end[1]) + 1)]
        if start[1] == end[1]:
            self.decks = [Deck(start[1] + i, end[1])
                          for i in range(abs(start[0] - end[0]) + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column and deck.is_alive:
                return deck

    def fire(self, row, column):
        attacked_deck = self.get_deck(row, column)
        if attacked_deck is not None:
            attacked_deck.is_alive = False
            if not all(self.decks):
                self.is_drowned = True


class Battleship:

    @staticmethod
    def _validate_field(ships: list[tuple]) -> bool:
        if len(ships) != 10:
            raise ValueError("The total number of the ships should be 10")
        fleet = {
            "single_deck": 0, "double_deck": 0, "three_deck": 0,
            "four_deck": 0
        }
        for ship in ships:
            count_deck = abs((ship[1][0] - ship[0][0])
                             - (ship[1][1] - ship[0][1])) + 1
            if count_deck == 1:
                fleet["single_deck"] += 1
            elif count_deck == 2:
                fleet["double_deck"] += 1
            elif count_deck == 3:
                fleet["three_deck"] += 1
            elif count_deck == 4:
                fleet["four_deck"] += 1
        if fleet["single_deck"] != 4:
            raise ValueError("there should be 4 single-deck ships")
        if fleet["double_deck"] != 3:
            raise ValueError("there should be 3 double-deck ships")
        if fleet["three_deck"] != 2:
            raise ValueError("there should be 2 three-deck ships")
        if fleet["four_deck"] != 1:
            raise ValueError("there should be 1 four-deck ship")
        # TODO: need add check locate ships

    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.field = {}
        self._validate_field(ships)
        for coordinates_ship in ships:
            ship = Ship(coordinates_ship[0], coordinates_ship[1])
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    # def __str__(self):
    #     return '\n'.join([' '.join(['~' for _ in range(10)])
    #                       for _ in range(10)])

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
print(battle_ship.field)
