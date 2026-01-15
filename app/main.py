from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(min(start[0], end[0]),
                         max(start[0], end[0]) + 1):
            for column in range(min(start[1], end[1]),
                                max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> None | Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break

        self.is_drowned = all(not deck.is_alive for deck in self.decks)
        return self.is_drowned

    def is_deck_alive(self, row: int, column: int) -> bool:
        return any(deck.row == row
                   and deck.column == column
                   and deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: tuple) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.ships = []
        self._field(ships)
        self._validate_field()

    def _field(self, ships: tuple) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> Any:
        size_of_ships = [len(ship.decks) for ship in self.ships]
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10!")
        if size_of_ships.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships!")
        if size_of_ships.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships!")
        if size_of_ships.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships!")
        if size_of_ships.count(4) != 1:
            raise ValueError("There should be 1 four-deck ships!")

        for ship in self.ships:
            for deck in ship.decks:
                neighbors = [
                    (row, column)
                    for row in range(max(0, deck.row - 1),
                                     min(10, deck.row + 2))
                    for column in range(max(0, deck.column - 1),
                                        min(10, deck.column + 2))
                    if (row, column) != (deck.row, deck.column)
                ]
                for neighbor in neighbors:
                    if (neighbor in self.field
                            and self.field[neighbor] != ship):
                        raise ValueError("ships shouldn't be"
                                         " located in the neighboring cells")

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        row, column = location
        if (row, column) not in self.field:
            return "Miss!"

        ship = self.field[(row, column)]
        is_drowned = ship.fire(row, column)

        if is_drowned:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = None
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for (row, column), ship in self.field.items():
            if ship:
                if ship.is_deck_alive(row, column):
                    field[row][column] = "O"
                else:
                    field[row][column] = "*"
            else:
                field[row][column] = "x"

        for row in field:
            print(" " + "  ".join(row))
