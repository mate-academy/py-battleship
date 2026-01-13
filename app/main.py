from typing import List, Tuple, Optional


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
        is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        start_row, start_col = start
        end_row, end_col = end

        r_start = min(start_row, end_row)
        r_end = max(start_row, end_row)
        c_start = min(start_col, end_col)
        c_end = max(start_col, end_col)

        for row in range(r_start, r_end + 1):
            for column in range(c_start, c_end + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError(
                        f"Ship collision at ({deck.row}, {deck.column})"
                    )
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location

        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(row, col)

        if ship.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"

    def print_field(self) -> None:
        print("Field state:")
        for row in range(10):
            row_str = ""
            for column in range(10):
                if (row, column) not in self.field:
                    row_str += " ~ "
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)

                    if deck is None:
                        continue

                    if ship.is_drowned:
                        row_str += " x "
                    elif not deck.is_alive:
                        row_str += " * "
                    else:
                        row_str += u" \u25A1 "
            print(row_str)
        print("-" * 30)

    def _validate_field(self) -> None:
        ships_set = set(self.field.values())

        if len(ships_set) != 10:
            raise ValueError(
                f"Invalid number of ships: {len(ships_set)}. Expected 10."
            )

        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in ships_set:
            length = len(ship.decks)
            if length in ship_counts:
                ship_counts[length] += 1
            else:
                raise ValueError(f"Invalid ship length found: {length}")

        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}
        if ship_counts != expected_counts:
            raise ValueError(
                f"Invalid fleet composition: {ship_counts}. "
                f"Expected {expected_counts}"
            )

        for (row, column), current_ship in self.field.items():
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    if d_row == 0 and d_col == 0:
                        continue

                    neighbor_pos = (row + d_row, column + d_col)

                    if neighbor_pos in self.field:
                        neighbor_ship = self.field[neighbor_pos]
                        if neighbor_ship is not current_ship:
                            raise ValueError(
                                f"Ships are touching at ({row}, {column}) "
                                f"and {neighbor_pos}"
                            )
