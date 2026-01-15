from typing import Tuple, List


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        if self.is_alive:
            return "□"
        return "*"


class Ship:
    def __init__(self,
                 start: Tuple[int],
                 end: Tuple[int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if abs(self.start[0] - self.end[0]) > 0:
            self.decks = {
                (x, self.start[1]): Deck(x, self.start[1])
                for x
                in range(self.start[0], self.end[0] + 1)}
        else:
            self.decks = {
                (self.start[0], y): Deck(self.start[0], y)
                for y
                in range(self.start[1], self.end[1] + 1)
            }

    def __len__(self) -> int:
        return len(self.decks)

    def __str__(self) -> str:
        if self.is_drowned:
            return "x" * len(self)
        return "".join(deck.__str__() for deck in self.decks)

    def __repr__(self) -> str:
        return f"Ship: ({self.start}, {self.end})"

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        if not self.is_drowned:
            hit_deck = self.get_deck(row, column)
            hit_deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks.values()):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [
            Ship(coordinates[0], coordinates[-1])
            for coordinates in ships
        ]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks.values()
        }

    def _validate_field(self) -> None:
        conditions = [
            len(self.ships) == 10,
            sum(ship for ship in self.ships if len(ship) == 1) == 4,
            sum(ship for ship in self.ships if len(ship) == 2) == 3,
            sum(ship for ship in self.ships if len(ship) == 3) == 2,
            sum(ship for ship in self.ships if len(ship) == 4) == 1
        ]
        if not all(conditions):
            raise ValueError("There should be total of 10 ships:\n"
                             "4 single-deck ships;"
                             "3 double-deck ships;"
                             "2 three-deck ships;"
                             "1 four-deck ship.")

    def __str__(self) -> str:
        matrix = [["~" for _ in range(10)] for _ in range(10)]
        for cell in self.field.keys():
            ship = self.field[cell]
            if ship.is_drowned:
                matrix[cell[0]][cell[1]] = "x"
            else:
                matrix[cell[0]][cell[1]] = str(ship.get_deck(cell[0], cell[1]))
        matrix = "\n".join(["   ".join(row) for row in matrix])
        return matrix

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field.keys():
            return self.field[location].fire(location[0], location[1])
        else:
            return "Miss!"
