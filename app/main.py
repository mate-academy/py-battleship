from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(
            self, start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start: Tuple[int, int] = start
        self.end: Tuple[int, int] = end
        self.is_drowned: bool = is_drowned
        self.decks: List[Deck] = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        (r1, c1), (r2, c2) = self.start, self.end

        if r1 == r2:
            return [Deck(r1, c) for c in range(min(c1, c2), max(c1, c2) + 1)]
        elif c1 == c2:
            return [Deck(r, c1) for r in range(min(r1, r2), max(r1, r2) + 1)]
        else:
            raise ValueError("Ship must be horizontal or vertical")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> Optional[str]:
        deck = self.get_deck(row, column)
        if deck is None:
            return None

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = [Ship(start, end) for start, end in ships]

        self.field: Dict[Tuple[int, int], Ship] = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships.")

        lengths = [len(ship.decks) for ship in self.ships]

        if lengths.count(1) != 4:
            raise ValueError("There must be 4 single-deck ships.")
        if lengths.count(2) != 3:
            raise ValueError("There must be 3 double-deck ships.")
        if lengths.count(3) != 2:
            raise ValueError("There must be 2 three-deck ships.")
        if lengths.count(4) != 1:
            raise ValueError("There must be 1 four-deck ship.")

        occupied = set(self.field.keys())

        for row, col in occupied:
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    new_row = row + d_row
                    new_col = col + d_col
                    if (
                        (new_row, new_col) in occupied
                        and (new_row, new_col) != (row, col)
                    ):
                        ship1 = self.field[(row, col)]
                        ship2 = self.field[(new_row, new_col)]
                        if ship1 is not ship2:
                            raise ValueError(
                                "Ships cannot touch each other,"
                                "even diagonally."
                            )

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location

        if (row, col) not in self.field:
            return "Miss!"

        ship = self.field[(row, col)]
        result = ship.fire(row, col)
        return result if result is not None else "Miss!"

    def print_field(self) -> None:
        grid: List[List[str]] = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                if ship.is_drowned:
                    grid[deck.row][deck.column] = "x"
                elif not deck.is_alive:
                    grid[deck.row][deck.column] = "*"
                else:
                    grid[deck.row][deck.column] = "□"

        for row in grid:
            print(" ".join(row))
        print()
