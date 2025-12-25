from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.start: Tuple[int, int] = start
        self.end: Tuple[int, int] = end
        self.is_drowned: bool = is_drowned
        self.decks: List[Deck] = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        r1, c1 = self.start
        r2, c2 = self.end
        if r1 == r2:
            return [Deck(r1, c) for c in range(min(c1, c2), max(c1, c2) + 1)]
        elif c1 == c2:
            return [Deck(r, c1) for r in range(min(r1, r2), max(r1, r2) + 1)]
        else:
            raise ValueError("Ships must be placed either horizontally "
                             "or vertically.")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            # This should not happen if called correctly from Battleship
            raise ValueError(f"Deck at ({row}, {column}) not found in ship")

        if not deck.is_alive:
            return "Already hit!"

        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int],
                                         Tuple[int, int]]]) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []

        max_row = 0
        max_col = 0

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
                max_row = max(max_row, deck.row)
                max_col = max(max_col, deck.column)

        self.size = max(max_row, max_col) + 1  # Assuming 0-based indexing

    def fire(self, location: Tuple[int, int]) -> str:
        row, column = location
        if (row, column) not in self.field:
            return "Miss!"

        ship = self.field[(row, column)]
        return ship.fire(row, column)

    def print_field(self) -> None:
        grid: List[List[str]] = [["~" for _ in range(self.size)]
                                 for _ in range(self.size)]

        for (r, c), ship in self.field.items():
            deck = ship.get_deck(r, c)
            if deck:
                if ship.is_drowned:
                    grid[r][c] = "x"
                elif not deck.is_alive:
                    grid[r][c] = "*"
                else:
                    grid[r][c] = "□"

        for row in grid:
            print(" ".join(row))

    def remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)
