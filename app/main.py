from typing import Any

# _test_deck = [
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
#     ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
# ]


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(
            self, start: tuple, end: tuple,
            is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        r1, c1 = start
        r2, c2 = end
        row_min, row_max = min(r1, r2), max(r1, r2)
        col_min, col_max = min(c1, c2), max(c1, c2)
        if r1 == r2:
            for col in range(col_min, col_max + 1):
                self.decks.append(Deck(r1, col))
        elif c1 == c2:
            for row in range(row_min, row_max + 1):
                self.decks.append(Deck(row, c1))

    def get_deck(self, row: int, column: int) -> Any:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def check_status(self) -> None:
        is_alive = any(d.is_alive for d in self.decks)
        if not is_alive:
            self.is_drowned = True

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            self.check_status()
            if self.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = []
        self.field = {}
        for ship in ships:
            ship_instance = Ship(*ship)
            self.ships.append(ship_instance)
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        else:
            return "Miss!"

    def print_field(self) -> str:
        battlefield = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"] * 10]
        for deck_row, deck_column in self.field.keys():
            battlefield[deck_row][deck_column] = u"\u25A1"

        for ship in self.ships:
            if ship.is_drowned:
                for deck in ship.decks:
                    battlefield[deck.row][deck.column] = "X"
            else:
                for deck in ship.decks:
                    if not deck.is_alive:
                        battlefield[deck.row][deck.column] = "*"

        string_field = ""
        for deck_row in battlefield:
            string_field += " ".join(deck_row)
            string_field += "\n"

        return string_field
