from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def create_deck(self) -> None:
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        else:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        if fired_deck:
            fired_deck.is_alive = False
        print(self.decks)
        self.is_drowned = not any([deck.is_alive for deck in self.decks])
        print("drowned", self.is_drowned)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self.ships = ships
        # Create a dict `self.field`. Its keys are tuples - the coordinates
        # of the non-empty cells, A value for each cell is a reference to the
        # ship which is located in it

    def fire(self, location: tuple) -> str:
        # This function should check whether the location is a key in the
        # `self.field`. If it is, then it should check if this cell
        # is the last alive in the ship or not.
        for key, value in self.field.items():
            if location[0] in range(key[0][0], key[1][0] + 1)\
                    and location[1] in range(key[0][1], key[1][1] + 1):
                value.create_deck()
                value.fire(location[0], location[1])
                if value.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"


    # def set_ships(self):
    #     for ship in self.ships:
    #
    #         print(ship[0], ship[1])





    # @staticmethod
    # def battlefield() -> list:
    #     return [["~" for _ in range(10)] for _ in range(10)]
    #
    # def print_field(self) -> None:
    #     for row in self.location:
    #         print(" ".join(row))




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

print(battle_ship.fire((0, 4))) #miss
print(battle_ship.fire((0, 5))) # == "Hit!"
print(battle_ship.fire((0, 6))) #== sunk

