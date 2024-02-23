class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    decks = []

    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks.append(Deck(start, end, is_drowned))

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    field = {}

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
        #TODO: need add check locate ships


    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self._validate_field(ships)
        for ship in ships:
            start, end = ship
            self.field[ship] = Ship(start, end)

    def __str__(self):
        return '\n'.join([' '.join(['~' for _ in range(10)])
                          for _ in range(10)])

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
print(battle_ship)
