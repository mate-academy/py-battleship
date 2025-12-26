from typing import List, Tuple, Optional


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True,
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def coordinates(self) -> Tuple[int, int]:
        return self.row, self.column


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> None:
        self.decks: List[Deck] = self._generate_decks(start, end)

    def _generate_decks(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> List[Deck]:
        r1, c1 = start
        r2, c2 = end
        if r1 == r2:
            return [
                Deck(r1, c)
                for c in range(min(c1, c2), max(c1, c2) + 1)
            ]
        if c1 == c2:
            return [
                Deck(r, c1)
                for r in range(min(r1, r2), max(r1, r2) + 1)
            ]
        raise ValueError("Ships must be placed horizontally or vertically.")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        if deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                return "Sunk!"
            return "Hit!"
        return "Hit!"  # Repeated shot on already hit deck


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        self._place_ships(ships)

    def _place_ships(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    ) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                coord = deck.coordinates()
                if coord in self.field:
                    raise ValueError(f"Overlapping ships at {coord}")
                self.field[coord] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        return ship.fire(*location)
