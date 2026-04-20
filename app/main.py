from typing import Optional


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
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
        self.is_drowned = is_drowned
        self.decks = []

        # Обчислюємо межі, щоб уникнути довгих рядків (E501)
        r_start, r_end = start[0], end[0]
        c_start, c_end = start[1], end[1]

        for row_idx in range(min(r_start, r_end), max(r_start, r_end) + 1):
            for col_idx in range(min(c_start, c_end), max(c_start, c_end) + 1):
                self.decks.append(Deck(row_idx, col_idx))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


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
        return target_ship.fire(location[0], location[1])
