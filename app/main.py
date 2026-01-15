from typing import List, Tuple, Optional, Dict


class Deck:
    def __init__(
        self,
        row_index: int,
        col_index: int,
        is_alive: bool = True
    ) -> None:
        self.row_index = row_index
        self.col_index = col_index
        self.is_alive = is_alive

    def fire(self) -> None:
        self.is_alive = False

    def __repr__(self) -> str:
        return "□" if self.is_alive else "x"


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> None:
        self.is_drowned: bool = False
        self.decks: List[Deck] = self.create_decks(start, end)
        if not self.decks:
            raise ValueError(f"Invalid ship: {start}-{end}")

    @staticmethod
    def create_decks(
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> List[Deck]:
        r1, c1 = start
        r2, c2 = end

        if r1 != r2 and c1 != c2:
            raise ValueError(f"Diagonal ships are not allowed: {start}-{end}")

        row_start, row_end = min(r1, r2), max(r1, r2)
        col_start, col_end = min(c1, c2), max(c1, c2)

        if row_start == row_end:
            return [Deck(row_start, c) for c in range(col_start, col_end + 1)]
        return [Deck(r, col_start) for r in range(row_start, row_end + 1)]

    def get_deck(self, row_index: int, col_index: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row_index == row_index and deck.col_index == col_index:
                return deck
        return None

    def status(self) -> str:
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"

    def fire(self, row_index: int, col_index: int) -> str:
        deck = self.get_deck(row_index, col_index)
        if deck:
            if deck.is_alive:
                deck.fire()
            return self.status()
        return ""  # Battleship.fire вернёт "Miss!"


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Tuple[int, int], Deck] = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                if not (0 <= deck.row_index <= 9 and 0 <= deck.col_index <= 9):
                    raise ValueError(
                        f"Deck out of bounds: {deck.row_index}, "
                        f"{deck.col_index}"
                    )
                if (deck.row_index, deck.col_index) in self.field:
                    raise ValueError(
                        f"Overlapping ships at {deck.row_index}, "
                        f"{deck.col_index}"
                    )
                self.field[(deck.row_index, deck.col_index)] = deck
            self.ships.append(ship)

    def fire(self, location: Tuple[int, int]) -> str:
        row_index, col_index = location
        deck = self.field.get((row_index, col_index))
        if not deck:
            return "Miss!"
        ship = next(s for s in self.ships if deck in s.decks)
        return ship.fire(row_index, col_index)

    def print_field(self) -> None:
        grid = [["~"] * 10 for _ in range(10)]
        for (r, c), deck in self.field.items():
            if deck.is_alive:
                grid[r][c] = "□"
            else:
                ship = next(s for s in self.ships if deck in s.decks)
                grid[r][c] = "x" if ship.is_drowned else "*"
        for row in grid:
            print(" ".join(row))

    def _validate_field(self) -> None:
        # Проверка состава флота и соседних клеток
        count_by_size = {}
        for ship in self.ships:
            size = len(ship.decks)
            count_by_size[size] = count_by_size.get(size, 0) + 1

        if count_by_size.get(1, 0) != 4 or \
           count_by_size.get(2, 0) != 3 or \
           count_by_size.get(3, 0) != 2 or \
           count_by_size.get(4, 0) != 1:
            raise ValueError("Invalid fleet composition")

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        occupied = set(self.field.keys())
        for row_index, col_index in occupied:
            for d_row, d_col in directions:
                neighbor = (row_index + d_row, col_index + d_col)
                if neighbor in occupied and neighbor != (row_index, col_index):
                    raise ValueError(
                        f"Ships too close at {row_index}, {col_index} "
                        f"and {neighbor[0]}, {neighbor[1]}"
                    )
