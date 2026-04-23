from typing import List, Tuple, Set, Optional


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
        self.is_drowned = is_drowned
        self.decks: List[Deck] = []
        row_step = 1 if end[0] > start[0] else (-1 if end[0] < start[0] else 0)
        col_step = 1 if end[1] > start[1] else (-1 if end[1] < start[1] else 0)
        current_row, current_col = start
        if row_step == 0 and col_step == 0:
            self.decks.append(Deck(start[0], start[1]))
        else:
            while (current_row, current_col) != (
                    end[0] + row_step, end[1] + col_step
            ):
                self.decks.append(Deck(current_row, current_col))
                if row_step == 0 and col_step == 0:
                    break
                current_row += row_step
                current_col += col_step

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        for ship_data in ships:
            start = ship_data[0]
            end = ship_data[1]
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        if not self._validate_field():
            raise ValueError("Invalid ship placement")

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        print("  " + " ".join(map(str, range(10))))
        for row in range(10):
            row_str = f"{row} "
            for column in range(10):
                coords = (row, column)
                if coords in self.field:
                    ship = self.field[coords]
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        row_str += "x "
                    elif not deck.is_alive:
                        row_str += "* "
                    else:
                        row_str += "□ "
                else:
                    row_str += "~ "
            print(row_str)

    def _validate_field(self) -> bool:
        visited: Set[Tuple[int, int]] = set()
        ships_found: List[int] = []
        for row, column in self.field:
            if (row, column) not in visited:
                ship_coords = self._get_ship_coords(row, column)
                if self._has_neighbors(ship_coords):
                    return False
                ships_found.append(len(ship_coords))
                visited.update(ship_coords)
        expected_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        return sorted(ships_found) == expected_ships

    def _get_ship_coords(self, row: int, column: int) -> List[Tuple[int, int]]:
        ship: List[Tuple[int, int]] = []
        stack = [(row, column)]
        while stack:
            curr_r, curr_c = stack.pop()
            if (curr_r, curr_c) not in ship:
                ship.append((curr_r, curr_c))
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = curr_r + dr, curr_c + dc
                    if (nr, nc) in self.field and (nr, nc) not in ship:
                        stack.append((nr, nc))
        return ship

    def _has_neighbors(self, ship_coords: List[Tuple[int, int]]) -> bool:
        for row, column in ship_coords:
            for d_row in [-1, 0, 1]:
                for d_column in [-1, 0, 1]:
                    if d_row == 0 and d_column == 0:
                        continue
                    n_row, n_column = row + d_row, column + d_column
                    if ((n_row, n_column) in self.field
                            and (n_row, n_column) not in ship_coords):
                        return True
        return False
