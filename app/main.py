from typing import Tuple, Dict, List, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned: bool = is_drowned
        self.decks: List[Deck] = []

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))
        else:
            raise ValueError("Ships must be horizontal or vertical")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck: Optional[Deck] = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        if not deck.is_alive:
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) \
            -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        for start, end in ships:
            ship: Ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        r, c = location
        if (r, c) not in self.field:
            return "Miss!"
        ship: Ship = self.field[(r, c)]
        return ship.fire(r, c)
