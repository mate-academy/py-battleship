class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        row1, col1 = start
        row2, col2 = end

        row_min, row_max = min(row1, row2), max(row1, row2)
        col_min, col_max = min(col1, col2), max(col1, col2)

        if row_min == row_max:
            for col_idx in range(col_min, col_max + 1):
                self.decks.append(Deck(row_min, col_idx))
        elif col_min == col_max:
            for row_idx in range(row_min, row_max + 1):
                self.decks.append(Deck(row_idx, col_min))
        else:
            raise ValueError("Diagonal ships are not allowed.")

    def get_deck(self, row: int, column: int) -> "Deck | None":
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False

        if not any(d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row, column = location

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row_idx in range(10):
            row_symbols = []
            for col_idx in range(10):
                if (row_idx, col_idx) in self.field:
                    ship = self.field[(row_idx, col_idx)]
                    deck = ship.get_deck(row_idx, col_idx)

                    if deck is None:
                        continue

                    if ship.is_drowned:
                        row_symbols.append("x")
                    elif not deck.is_alive:
                        row_symbols.append("*")
                    else:
                        row_symbols.append(u"\u25A1")
                else:
                    row_symbols.append("~")

            print("\t".join(row_symbols))
        print()

    def _validate_field(self) -> None:
        unique_ships = list(set(self.field.values()))

        if len(unique_ships) != 10:
            raise ValueError(
                f"Expected exactly 10 ships, found {len(unique_ships)}."
            )

        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in unique_ships:
            size = len(ship.decks)
            if size not in ship_counts:
                raise ValueError(
                    f"Invalid ship size: {size}. Must be 1-4 decks."
                )
            ship_counts[size] += 1

        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}
        if ship_counts != expected_counts:
            raise ValueError(
                f"Invalid fleet. Expected {expected_counts}, "
                f"got {ship_counts}."
            )

        for (row, col), current_ship in self.field.items():
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    if d_row == 0 and d_col == 0:
                        continue

                    neighbor_loc = (row + d_row, col + d_col)

                    if neighbor_loc in self.field:
                        neighbor_ship = self.field[neighbor_loc]
                        if neighbor_ship is not current_ship:
                            raise ValueError(
                                "Ships cannot touch! Conflict near "
                                f"({row}, {col}) and {neighbor_loc}."
                            )
