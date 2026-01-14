from typing import Tuple, List, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            if start[1] > end[1]:
                row = start[0]
                for col in range(end[1], start[1] + 1):
                    self.decks.append(Deck(row, col))
                return

            row = start[0]
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
            return

        if start[1] == end[1]:
            if start[0] > end[0]:
                col = start[1]
                for row in range(end[0], start[0] + 1):
                    self.decks.append(Deck(row, col))
                return

            col = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, col))
            return

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True

    def __repr__(self) -> str:
        return f"{self.decks}"


class Battleship:
    def __init__(self, ships: List[Ship]) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_ships(self) -> bool:
        for deck, ship in self.field.items():
            row, col = deck
            if not (0 <= row < 10 and 0 <= col < 10):
                print(
                    f"Invalid coordinates for ship at {deck}: out of bounds."
                )
                return False

        check_cross_deck = set()
        for deck in self.field.keys():
            if deck in check_cross_deck:
                print(f"Deck {deck} is already in use.")
                return False
            check_cross_deck.add(deck)

        print("All ships are correctly placed.")
        return True

    def print_field(self) -> None:
        matrix_field = []

        for row_item in range(10):
            row = []
            for col_item in range(10):
                if (row_item, col_item) in self.field:
                    ship = self.field[(row_item, col_item)]
                    deck = ship.get_deck(row_item, col_item)
                    if ship.is_drowned:
                        row.append("x")
                    elif not deck.is_alive:
                        row.append("*")
                    else:
                        row.append("□")
                else:
                    row.append("~")
            matrix_field.append("  ".join(row))

        for row in matrix_field:
            print(row)

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        if not (0 <= row < 10 and 0 <= col < 10):
            return "Invalid coordinates! Out of bounds."

        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
