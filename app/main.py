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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        # Create decks and save them to a list `self.decks`
        self.decks: list = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        deck_fire = self.get_deck(row, column)
        deck_fire.is_alive = False

        # And update the `is_drowned` value if it's needed
        is_alive: bool = False
        for deck in self.decks:
            if deck.is_alive:
                is_alive = True
                break
        if not is_alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships: list = []
        self.field: dict = {}
        for ship_coord in ships:
            ship = Ship(*ship_coord)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        try:
            self._validate_field()
        except ValueError as verr:
            print(verr)
            exit()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field.keys():
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            if not ship.get_deck(*location).is_alive:
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        end_value: str = "     "
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field.keys():
                    print("~", end=end_value)
                else:
                    for coord, ship in self.field.items():
                        if (row, col) == coord:
                            if ship.is_drowned:
                                print("x", end=end_value)
                            else:
                                for deck in ship.decks:
                                    if (row, col) == (deck.row, deck.column):
                                        if deck.is_alive:
                                            print(u"\u25A1", end=end_value)
                                        else:
                                            print("*", end=end_value)
            print("\n")

    def _validate_field(self) -> None:
        ships_count: dict = {1: 0, 2: 0, 3: 0, 4: 0}

        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10!")

        for ship1 in self.ships:
            deck_count = sum(
                1 for ship2 in self.field.values() if ship2 == ship1
            )
            ships_count[deck_count] += 1
        if ships_count[1] != 4:
            raise ValueError("There should be 4 single-deck ships!")
        if ships_count[2] != 3:
            raise ValueError("There should be 3 double-deck ships!")
        if ships_count[3] != 2:
            raise ValueError("There should be 2 three-deck ships!")
        if ships_count[4] != 1:
            raise ValueError("There should be 1 four-deck ship!")

        for ship1 in self.ships:
            for ship2 in self.ships:
                if ship1 != ship2:
                    s10: int = ship1.start[0] - 1 if ship1.start[0] > 1 else 0
                    s11: int = ship1.start[1] - 1 if ship1.start[1] > 1 else 0
                    e10: int = ship1.end[0] + 1 if ship1.end[0] < 8 else 9
                    e11: int = ship1.end[1] + 1 if ship1.end[1] < 8 else 9
                    s20: int = ship2.start[0]
                    s21: int = ship2.start[1]
                    e20: int = ship2.end[0]
                    e21: int = ship2.end[1]
                    row_conflict: bool = s10 <= s20 <= e10 or s10 <= e20 <= e10
                    col_conflict: bool = s11 <= s21 <= e11 or s11 <= e21 <= e11
                    if row_conflict and col_conflict:
                        raise ValueError("Ships shouldn't be located in "
                                         "the neighboring cells (even if "
                                         "cells are neighbors by diagonal)!")
