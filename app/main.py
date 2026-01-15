from typing import Any, List, Dict


class Deck:
    def __init__(self, row: (int, int),
                 column: (int, int),
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: (int, int),
                 end: (int, int),
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.decks = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        x1, y1 = self.start
        x2, y2 = self.end
        decks = []
        if x1 == x2:
            for column in range(y1, y2 + 1):
                decks.append(Deck(x1, column))
        elif y1 == y2:
            for row in range(x1, x2 + 1):
                decks.append(Deck(row, y1))
        return decks

    def get_deck(self, row: (int, int), column: (int, int)) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> Any:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all([deck.is_alive is False for deck in self.decks]):
                self.is_drowned = True
        return self


class Battleship:
    def __init__(self, ships: list[tuple[int, int]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(ship_coord[0], ship_coord[1])
                      for ship_coord in ships]
        self.field = self._make_ship()

    def _make_ship(self) -> Dict:
        field_ship = {}
        for ship in self.ships:
            for deck in ship.decks:
                field_ship[(deck.row, deck.column)] = ship
        return field_ship

    def fire(self, location: (int, int)) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        if location in self.field:
            ship = self.field[location]
            hit = ship.fire(*location)
            if hit:
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for i in range(10)] for j in range(10)]
        for i_coord in range(10):
            for j_coord in range(10):
                lock = (i_coord, j_coord)
                if lock in self.field:
                    ship = self.field[lock]
                    deck = ship.get_deck(*lock)
                    if ship.is_drowned:
                        field[deck.row][deck.column] = "x"
                    elif not deck.is_alive:
                        field[deck.row][deck.column] = "*"
                    else:
                        field[deck.row][deck.column] = u"\u25A1"

        for i_coord in range(10):
            for j_coord in range(10):
                print(field[i_coord][j_coord], end=" ")
            print()

    def validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10")

        count_decks = [len(ship.decks) for ship in set(self.field.values())]
        if count_decks.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships")
        if count_decks.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships")
        if count_decks.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships")
        if count_decks.count(4) != 1:
            raise ValueError("There should be 1 four-deck ship")

        for row, column in self.field:
            ship = self.field[row, column]
            for x_cell in range(-1, 2):
                for y_cell in range(-1, 2):
                    next_cell = (row + x_cell, column + y_cell)

                    if (next_cell in self.field
                            and self.field[next_cell] != ship):
                        raise ValueError(f"Ships {next_cell} shouldn't be "
                                         f"located in the neighboring "
                                         f"cells {row, column}")
