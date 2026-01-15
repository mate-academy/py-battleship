from typing import List, Tuple, Dict


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> None:
        self.decks: List[Deck] = []

        row1, col1 = start
        row2, col2 = end

        if row1 == row2:  # horizontal
            for col in range(min(col1, col2), max(col1, col2) + 1):
                self.decks.append(Deck(row1, col))
        elif col1 == col2:  # vertical
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, col1))
        else:
            raise ValueError(
                "Ships must be placed horizontally or vertically."
            )

    def get_deck(self, row: int, col: int) -> Deck | None:
        for deck_item in self.decks:
            if deck_item.row == row and deck_item.column == col:
                return deck_item
        return None

    def fire(self, row: int, col: int) -> str:
        deck_item = self.get_deck(row, col)
        if not deck_item:
            return "Miss!"

        deck_item.is_alive = False
        if all(not d.is_alive for d in self.decks):
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
                 ) -> None:
        self.size: int = 10
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []

        for start, end in ships:
            ship = Ship(start, end)
            self._add_ship(ship)

        self._validate_field()

    def _add_ship(self, ship: Ship) -> None:
        for deck_item in ship.decks:
            if (deck_item.row, deck_item.column) in self.field:
                raise ValueError("Ships cannot overlap.")
            self.field[(deck_item.row, deck_item.column)] = ship
        self.ships.append(ship)

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        row, col = location
        ship = self.field[location]
        return ship.fire(row, col)

    def print_field(self) -> None:
        for row_index in range(self.size):
            row_symbols: List[str] = []
            for col_index in range(self.size):
                ship = self.field.get((row_index, col_index))
                if not ship:
                    row_symbols.append("~")
                else:
                    deck_item = ship.get_deck(row_index, col_index)
                    if deck_item and deck_item.is_alive:
                        row_symbols.append("□")
                    elif deck_item and not deck_item.is_alive:
                        if any(dd.is_alive for dd in ship.decks):
                            row_symbols.append("*")
                        else:
                            row_symbols.append("x")
            print(" ".join(row_symbols))

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

        occupied = {(deck_item.row, deck_item.column)
                    for ship in self.ships for deck_item in ship.decks}
        for row_index, col_index in occupied:
            for delta_row in (-1, 0, 1):
                for delta_col in (-1, 0, 1):
                    if delta_row == delta_col == 0:
                        continue
                    new_row, new_col = (
                        row_index + delta_row,
                        col_index + delta_col
                    )
                    if (new_row, new_col) in self.field:
                        neighbor_ship = self.field[(new_row, new_col)]
                        current_ship = self.field[(row_index, col_index)]
                        if neighbor_ship is not current_ship:
                            raise ValueError(
                                "Ships cannot touch each other, "
                                "even diagonally."
                            )
