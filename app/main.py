from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        in_row = end[0] - start[0] + 1
        in_column = end[1] - start[1] + 1
        for i in range(in_row):
            for _ in range(in_column):
                # print((start[0] + i, start[1] + _))
                self.decks.append(Deck(start[0] + i, start[1] + _))
        # print(self.decs)
        # Create decks and save them to a list `self.decks`

    def get_deck(self, row: int, column: int) -> Deck:
        return next(
            deck for deck in self.decks
            if deck.row == row and deck.column == column
        )
        # Find the corresponding deck in the list

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for i in range(len(ships)):
            ship = Ship(ships[i][0], ships[i][1])
            for _ in range(len(ship.decks)):
                self.field[(ship.decks[_].row, ship.decks[_].column)] = ship
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.


# Battleship(
#     ships=[
#         ((0, 0), (0, 3)),
#         ((0, 5), (0, 6)),
#         ((0, 8), (0, 9)),
#         ((2, 0), (4, 0)),
#         ((2, 4), (2, 6)),
#         ((2, 8), (2, 9)),
#         ((9, 9), (9, 9)),
#         ((7, 7), (7, 7)),
#         ((7, 9), (7, 9)),
#         ((9, 7), (9, 7)),
#     ]
# )
