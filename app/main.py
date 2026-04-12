from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        row_start, col_start = start
        row_end, col_end = end

        for row_idx in range(
            min(row_start, row_end), max(row_start, row_end) + 1
        ):
            for col_idx in range(
                min(col_start, col_end), max(col_start, col_end) + 1
            ):
                self.decks.append(Deck(row_idx, col_idx))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for start, end in ships:
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        target_ship = self.field[location]

        target_ship.fire(location[0], location[1])

        if target_ship.is_drowned:
            return "Sunk!"

        return "Hit!"
