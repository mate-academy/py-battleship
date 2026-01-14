from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, alive={self.is_alive})"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not _.is_alive for _ in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            return result
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = "□"
                else:
                    field[deck.row][deck.column] = "*" if not ship.is_drowned \
                        else "x"

        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) == 10:
            ships_count = {1: 0, 2: 0, 3: 0, 4: 0}

            for ship in self.ships:
                decks_count = len(ship.decks)
                if decks_count in ships_count:
                    ships_count[decks_count] += 1

            if ships_count != {1: 4, 2: 3, 3: 2, 4: 1}:
                raise ValueError("Invalid deck count.")
        else:
            raise ValueError("Should be 10 ships.")
        for ship in self.ships:
            for deck in ship.decks:
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        neighbor = (deck.row
                                    + row_offset, deck.column + col_offset)
                        if (neighbor in self.field
                                and self.field[neighbor] != ship):
                            raise ValueError("Ships should not be placed "
                                             "in neighboring cells.")
