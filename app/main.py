from typing import Dict, Iterable, List, Optional, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: List[Deck] = []

        start_row, start_column = start
        end_row, end_column = end

        self._validate_bounds(start_row, start_column)
        self._validate_bounds(end_row, end_column)

        if start_row == end_row:
            step = 1 if end_column >= start_column else -1
            for column in range(start_column, end_column + step, step):
                self._validate_bounds(start_row, column)
                self.decks.append(Deck(start_row, column))
        elif start_column == end_column:
            step = 1 if end_row >= start_row else -1
            for row in range(start_row, end_row + step, step):
                self._validate_bounds(row, start_column)
                self.decks.append(Deck(row, start_column))
        else:
            raise ValueError("Ships must be horizontal or vertical")

    @staticmethod
    def _validate_bounds(row: int, column: int) -> None:
        if not (0 <= row <= 9 and 0 <= column <= 9):
            raise ValueError(
                f"Coordinates ({row}, {column}) out of 10x10 field bounds"
            )

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is None or not deck.is_alive:
            return False

        deck.is_alive = False
        self.is_drowned = all(not d.is_alive for d in self.decks)
        return True


class Battleship:
    def __init__(
        self, ships: Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                coordinates = (deck.row, deck.column)
                if coordinates in self.field:
                    raise ValueError("Ships cannot overlap on the field")
                self.field[coordinates] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, column = location

        if not (0 <= row <= 9 and 0 <= column <= 9):
            raise ValueError(
                f"Shot coordinates ({row}, {column}) out of 10x10 field bounds"
            )

        ship = self.field.get(location)
        if ship is None:
            return "Miss!"

        hit = ship.fire(row, column)
        if not hit:
            return "Miss!"

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
