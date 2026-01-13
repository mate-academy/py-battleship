from typing import List, Tuple, Optional


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
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
        self.is_drowned = is_drowned
        self.decks = []

        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row:
            for col in range(min(start_col, end_col),
                             max(start_col, end_col) + 1):
                self.decks.append(Deck(start_row, col))

        else:
            for row in range(min(start_row, end_row),
                             max(start_row, end_row) + 1):
                self.decks.append(Deck(row, start_col))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None:
            return

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[
                Tuple[Tuple[int, int], Tuple[int, int]]
            ]
    ) -> None:
        self.field = {}
        self.ships = []
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        row, col = location

        if (row, col) not in self.field:
            return "Miss!"

        ship = self.field[(row, col)]
        ship.fire(row, col)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def _validate_field(
            self,
            ships: List[
                Tuple[
                    Tuple[int, int],
                    Tuple[int, int],
                ]
            ],
    ) -> None:
        if len(ships) != 10:
            raise ValueError(
                "There must be exactly 10 ships."
            )

        ship_sizes = {1: 0, 2: 3, 3: 2, 4: 1}
        found_sizes = {1: 0, 2: 0, 3: 0, 4: 0}

        occupied_cells = set()

        for start, end in ships:
            start_row, start_col = start
            end_row, end_col = end

            # Validate boundaries
            if not (
                    0 <= start_row <= 9
                    and 0 <= start_col <= 9
                    and 0 <= end_row <= 9
                    and 0 <= end_col <= 9
            ):
                raise ValueError(
                    "Ship coordinates must be between 0 and 9."
                )

            # Must be horizontal or vertical
            if start_row != end_row and start_col != end_col:
                raise ValueError(
                    "Ships must be placed horizontally or vertically."
                )

            # Ensure start <= end
            if start_row > end_row or start_col > end_col:
                raise ValueError(
                    "Ship start must be before its end."
                )

            # Build ship cells
            if start_row == end_row:
                size = end_col - start_col + 1
                cells = [
                    (start_row, col)
                    for col in range(start_col, end_col + 1)
                ]
            else:
                size = end_row - start_row + 1
                cells = [
                    (row, start_col)
                    for row in range(start_row, end_row + 1)
                ]

            if size not in found_sizes:
                raise ValueError("Invalid ship size.")

            found_sizes[size] += 1

            # Check adjacency
            for row_index, col_index in cells:
                neighbor_positions = [
                    (row_index + delta_row, col_index + delta_col)
                    for delta_row in (-1, 0, 1)
                    for delta_col in (-1, 0, 1)
                ]

                for neighbor_row, neighbor_col in neighbor_positions:
                    if (neighbor_row, neighbor_col) in occupied_cells:
                        raise ValueError(
                            "Ships cannot touch each other."
                        )

            occupied_cells.update(cells)

        if found_sizes != ship_sizes:
            raise ValueError("Incorrect ship composition.")

    def print_field(self) -> None:
        field_matrix = [["~" for _ in range(10)] for _ in range(10)]

        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)

            if ship.is_drowned:
                symbol = "x"
            elif not deck.is_alive:
                symbol = "*"
            else:
                symbol = "□"

            field_matrix[row][col] = symbol

        for row in field_matrix:
            print(" ".join(row))
