from typing import Union

from tabulate import tabulate

"""
~  empty
□ alive
* injured
x drowned
"""


# deck+deck+deck = Ship

class Deck:
    def __init__(self, row, column, is_alive=True):  # PART/COMPONENT
        self.row = row
        self.column = column
        self.is_alive = is_alive

    # def __repr__(self):
    #     return (f"{self.row} | {self.column} | "
    #             f"ALIVE | {self.is_alive} |")
    def __str__(self):
        return f"({self.row}, {self.column}, {self.is_alive})"


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False
                 ) -> None:  # WHOLE SHIP
        self.start = start
        self.end = end

        self.is_drowned = is_drowned
        # self.direction = None

        self.decks: [Deck] = []  # Deck/Decks of every Ship
        self.fill_decks()

    def fill_decks(self):
        if self.start == self.end:
            # self.direction = "single_point"  # □
            self.decks.append(Deck(row=self.start[0], column=self.start[1]))
        if self.start[0] == self.end[0]:
            # self.direction = "x"  # □ □ □
            self.decks = [Deck(row=self.start[0], column=coord) for coord
                          in range(self.start[1], self.end[1] + 1)]
            return
        # self.direction = "y"  # □
        self.decks = [Deck(row=coord, column=self.start[1]) for coord
                      in range(self.start[0], self.end[0] + 1)]
        self.decks.extend([Deck(row=self.start[0], column=self.start[1])] if self.start == self.end
                          else [Deck(row=self.start[0], column=coord) for coord in range(self.start[1], self.end[1] + 1)] if self.start[0] == self.end[0]
                          else [Deck(row=coord, column=self.start[1]) for coord in range(self.start[0], self.end[0] + 1)])

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None
        # Find the Deck instance by coords

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.decks.remove(deck)  # no need to remove, need to check status
            if len(self.decks) == 0:
                self.is_drowned = True

    def __repr__(self):
        return f"{self.start}{self.end}{self.is_drowned}"


class Battleship:
    def __init__(self, ships: list[tuple]):  # Whole game
        self.field = {}  # Create a dict `self.field`. # ((), (), ... ()) : self.Ship
        counter = 1
        for coord in ships:  # debug
            ship = Ship(start=coord[0], end=coord[1])
            # print(f"Ship # {counter}:\n{ship}\n")  # debug
            counter += 1  # debug
            for deck in ship.decks:
                # print(deck)
                self.field[deck] = ship
        # print(self.field)
        # self.validate_input()
        # self.print_field()
        # print(self.field)
        self.fire((7, 7))

    def fire(self, location: tuple):  # Loop is not needed. Just check:
        # if location in self.field:
        print(location)
        print(self.field)
        for coord, ship in self.field.items():
            point = (coord.row, coord.column)
            if point == location:
                ship.fire(*location)
                if ship.is_drowned is True:
                    return "Sunk!"
                else:
                    return "Hit!"
        return "Miss!"
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

    def print_field(self):  # Extra

        self.field = [["~" for column in range(10)] for field in range(10)]
        print(tabulate(self.field, tablefmt="grid"))

    def validate_input(self):  # Extra
        pass


if __name__ == '__main__':
    print("MAIN.PY -> print testing")
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
