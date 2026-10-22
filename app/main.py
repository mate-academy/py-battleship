from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other: Deck) -> bool:
        if isinstance(other, Deck):
            return self.row == other.row and self.column == other.column
        return False

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        start = Deck(start[0], start[1])
        end = Deck(end[0], end[1])
        start_copy = Deck(start.row, start.column)
        self.decks = []
        if start == end:
            self.decks = [Deck(start.row, start.column)]
            return
        elif start.row == end.row and start.column != end.column:
            difference = abs(end.column - start.column)
            part_to_increase = "start.column"
        else:
            difference = abs(end.row - start.row)
            part_to_increase = "start.row"
        for _ in range(difference):
            self.decks.append(Deck(start_copy.row, start_copy.column))
            if part_to_increase == "start.row":
                start_copy.row += 1
            if part_to_increase == "start.column":
                start_copy.column += 1
        self.decks.append(Deck(end.row, end.column))

    def __repr__(self) -> str:
        return f"Ship(decks={self.decks})"

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def count_alive_decks(self) -> int:
        alive_decks = 0
        for deck in self.decks:
            if deck.is_alive:
                alive_decks += 1
        return alive_decks

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        current_deck = self.get_deck(row, column)
        current_deck.is_alive = False
        quantity_alive_decks = self.count_alive_decks()
        if quantity_alive_decks == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            ship_object = Ship(ship[0], ship[1])
            for deck in ship_object.decks:
                deck_tuple = (deck.row, deck.column)
                self.field[deck_tuple] = ship_object
        self._validate_field()

    def __repr__(self) -> str:
        return f"Battleship(ships={self.field.values()})"

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            quantity_alive_decks = ship.count_alive_decks()
            ship.fire(location[0], location[1])
            if quantity_alive_decks == 1:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        external_matrix = []
        for _ in range(10):
            internal_matrix = []
            for _ in range(10):
                internal_matrix.append("~")
            external_matrix.append(internal_matrix)
        for ship in list(self.field.values()):
            for deck in ship.decks:
                if deck.is_alive:
                    external_matrix[deck.row][deck.column] = u"\u25A1"
                if ship.is_drowned:
                    external_matrix[deck.row][deck.column] = "x"
                if not ship.is_drowned and not deck.is_alive:
                    external_matrix[deck.row][deck.column] = "*"
        for row in external_matrix:
            print(row)

    def _validate_field(self) -> None:
        if len(set(self.field.values())) != 10:
            raise ValueError("Invalid field configuration!")
        has_4_single_deck_ships = 0
        has_3_double_deck_ships = 0
        has_2_three_deck_ships = 0
        has_1_four_deck_ships = 0
        for ship in set(self.field.values()):
            if len(ship.decks) == 1:
                has_4_single_deck_ships += 1
            if len(ship.decks) == 2:
                has_3_double_deck_ships += 1
            if len(ship.decks) == 3:
                has_2_three_deck_ships += 1
            if len(ship.decks) == 4:
                has_1_four_deck_ships += 1
        if has_4_single_deck_ships != 4:
            raise ValueError("there should be 4 single-deck ships!")
        if has_3_double_deck_ships != 3:
            raise ValueError("there should be 3 double-deck ships!")
        if has_2_three_deck_ships != 2:
            raise ValueError("there should be 2 three-deck ships!")
        if has_1_four_deck_ships != 1:
            raise ValueError("there should be 1 four-deck ship!")
        for ship in list(self.field.values()):
            for deck in ship.decks:
                one_up = Deck(deck.row - 1, deck.column)
                one_down = Deck(deck.row + 1, deck.column)
                one_left = Deck(deck.row, deck.column - 1)
                one_right = Deck(deck.row, deck.column + 1)
                one_left_up_diagonally = Deck(deck.row - 1, deck.column - 1)
                one_left_down_diagonally = Deck(deck.row + 1, deck.column - 1)
                one_right_up_diagonally = Deck(deck.row - 1, deck.column + 1)
                one_right_down_diagonally = Deck(deck.row + 1, deck.column + 1)
                all_sides = [
                    one_up,
                    one_down,
                    one_left,
                    one_right,
                    one_left_up_diagonally,
                    one_left_down_diagonally,
                    one_right_up_diagonally,
                    one_right_down_diagonally]
                for other_ship in list(self.field.values()):
                    if ship is other_ship:
                        continue
                    decks = other_ship.decks
                    results = [deck in decks for deck in all_sides]
                    if any(results):
                        raise ValueError(
                            "ships shouldn't"
                            " be located in the neighboring cells")
