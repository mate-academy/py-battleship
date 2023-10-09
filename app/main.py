from __future__ import annotations


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: int = True
    ) -> None:
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
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], i)
                for i in range(start[1], end[1] + 1)
            ]
        elif end[1] == start[1]:
            self.decks = [
                Deck(i, start[1])
                for i in range(start[0], end[0] + 1)
            ]
        else:
            raise ValueError("Wrong coordinates")

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for coordinates in ships:
            ship = Ship(coordinates[0], coordinates[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        # This function is for debugging
        # It prints the field in the console
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].is_drowned:
                        print("x", end=" ")
                    elif not (
                            self.field[
                                (row, column)
                            ].get_deck(row, column).is_alive):
                        print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> bool:
        ships = []
        decks_counting = {1: 0, 2: 0, 3: 0, 4: 0}
        for coordinate in self.field:
            if self.field[coordinate] not in ships:
                ships.append(self.field[coordinate])
        for ship in ships:
            decks_counting[len(ship.decks)] += 1
            if ship.start[0] == ship.end[0]:
                for i in range(ship.start[1] - 1, ship.end[1] + 2):
                    if ((ship.start[0] - 1, i) in self.field
                            or (ship.start[0] + 1, i) in self.field):
                        return False
                if ((ship.start[0], ship.start[1] - 1) in self.field
                        or ship.end[0], ship.end[1] + 1) in self.field:
                    return False
            elif ship.start[1] == ship.end[1]:
                for i in range(ship.start[0] - 1, ship.end[0] + 2):
                    if ((i, ship.start[1] - 1) in self.field
                            or (i, ship.start[1] + 1) in self.field):
                        return False
                if ((ship.start[0] - 1, ship.start[1]) in self.field
                        or (ship.end[0] + 1, ship.end[1]) in self.field):
                    return False

        if len(ships) == 10 and decks_counting == {1: 4, 2: 3, 3: 2, 4: 1}:
            return True
        return False
