from typing import List


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Alive: {self.is_alive}"

    def get_coordinate_in_tuple(self) -> tuple:
        return self.row, self.column

    def __eq__(self, other: tuple) -> bool:
        return (self.row, self.column) == other


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = [
            Deck(
                row=row_index,
                column=column_index
            )
            for row_index in range(self.start[0], self.end[0] + 1)
            for column_index in range(self.start[1], self.end[1] + 1)
        ]

    def __repr__(self) -> str:
        if len(self.decks) == 4:
            return "4-deck ship"
        elif len(self.decks) == 3:
            return "3-deck ship"
        elif len(self.decks) == 2:
            return "2-deck ship"
        return "1-deck ship"

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list +
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(
            start=ship[0],
            end=ship[1]
        ) for ship in ships]

        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def print_fields(self) -> None:
        for row in range(10):
            print()
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if (ship.get_deck(row, column).is_alive
                            and not ship.is_drowned):
                        print(" □ ", end="")
                    elif not ship.is_drowned:
                        print(" * ", end="")
                    else:
                        print(" x ", end="")
                else:
                    print(" ~ ", end="")
