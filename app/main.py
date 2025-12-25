from typing import Optional, Iterable


class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        row_idx1, col_idx1 = self.start
        row_idx2, col_idx2 = self.end

        if row_idx1 == row_idx2:
            c_min, c_max = sorted([col_idx1, col_idx2])
            cords = [(row_idx1, c) for c in range(c_min, c_max + 1)]
        elif col_idx1 == col_idx2:
            r_min, r_max = sorted([row_idx1, row_idx2])
            cords = [(r, col_idx1) for r in range(r_min, r_max + 1)]
        else:
            raise ValueError

        for row_idx, col_idx in cords:
            if not (0 <= row_idx <= 9 and 0 <= col_idx <= 9):
                raise ValueError

        self.decks = [Deck(row_idx, col_idx) for (row_idx, col_idx) in cords]

    def get_deck(self, row: int, column: int) -> Optional["Deck"]:

        for deck_obj in self.decks:
            if deck_obj.row == row and deck_obj.column == column:
                return deck_obj
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck is None:
            return "Miss!"
        elif not deck.is_alive:
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"
        deck.is_alive = False
        self.is_drowned = all(not d.is_alive for d in self.decks)
        if self.is_drowned:
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: Iterable[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:

        self.ships = [Ship(start, end) for (start, end) in ships]
        self.field = {}

        for ship in self.ships:
            for deck_cell in ship.decks:
                key = (deck_cell.row, deck_cell.column)
                if key in self.field:
                    raise ValueError
                self.field[key] = ship

    def fire(self, location: tuple[int, int]) -> str:

        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(*location)
