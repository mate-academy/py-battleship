from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks: List[Deck] = []
        self.is_drowned: bool = is_drowned

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))
        else:
            raise ValueError("Statek może być tylko poziomy lub pionowy.")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
        return self.is_drowned


class Battleship:
    def __init__(
            self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location

        if (row, col) not in self.field:
            return "Miss!"

        ship = self.field[(row, col)]
        deck = ship.get_deck(row, col)
        if deck is None or not deck.is_alive:
            return "Miss!"  # strzał w pustą lub już zniszczoną komórkę

        is_drowned = ship.fire(row, col)
        return "Sunk!" if is_drowned else "Hit!"
