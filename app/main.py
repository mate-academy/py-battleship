from __future__ import annotations


class ValidationError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple, is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
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

    def are_ships_neighbors(self, other_ship: Ship) -> bool:
        for deck1 in self.decks:
            for deck2 in other_ship.decks:
                if (abs(deck1.row - deck2.row) <= 1
                        and abs(deck1.column - deck2.column) <= 1):
                    return True
        return False

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all([not deck.is_alive for deck in self.decks])
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for coord in ships:
            self.field.update({coord: Ship(coord[0], coord[1])})

        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for coords, ship in self.field.items():
            ship_decks = ship.get_deck(location[0], location[1])
            if ship_decks is not None:
                return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        symbols = {"empty": "~", "alive": "\u25A1", "hit": "*", "drowned": "x"}

        matrix = [[symbols["empty"] for _ in range(10)] for _ in range(10)]

        for coords, ship in self.field.items():
            for deck in ship.decks:
                if ship.is_drowned is True:
                    matrix[deck.row][deck.column] = symbols["drowned"]
                elif deck.is_alive is False:
                    matrix[deck.row][deck.column] = symbols["hit"]
                elif deck.is_alive is True:
                    matrix[deck.row][deck.column] = symbols["alive"]

        for row in matrix:
            print(" ".join(row))

    def _are_ships_neighbors(self) -> bool:
        for ship1 in self.field.values():
            for ship2 in self.field.values():
                if ship1 != ship2 and Ship.are_ships_neighbors(ship1, ship2):
                    return True
        return False

    def _validate_field(self) -> bool:
        ships = sorted([len(ship.decks) for ship in self.field.values()])
        count_length_ship = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

        if count_length_ship != ships:
            raise ValidationError(
                """
                there should be 4 single-deck ships;
                there should be 3 double-deck ships;
                there should be 2 three-deck ships;
                there should be 1 four-deck ship;
                """)

        if len(self.field) != len(count_length_ship):
            raise ValidationError(
                "the total number of the ships should be 10;")

        if self._are_ships_neighbors():
            raise ValidationError("ships shouldn't be located "
                                  "in the neighboring cells "
                                  "(even if cells are neighbors by diagonal).")

