from collections import defaultdict


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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        start_row, start_col = start
        end_row, end_col = end

        if start_row == end_row:
            for col in range(
                    min(start_col, end_col),
                    max(start_col, end_col) + 1
            ):
                self.decks.append(Deck(start_row, col))

        elif start_col == end_col:
            for row in range(
                    min(start_row, end_row),
                    max(start_row, end_row) + 1
            ):
                self.decks.append(Deck(row, start_col))

        else:
            raise ValueError("Ship must be horizontal or vertical")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break
        self.is_drowned = all(not deck.is_alive for deck in self.decks)
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                coord = (deck.row, deck.column)
                if coord in self.field:
                    raise ValueError("Overlapping ships at: ", coord)
                self.field[coord] = ship
            self.ships.append(ship)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, col = location
        if (row, col) not in self.field:
            return "Miss!"
        ship = self.field[(row, col)]
        return ship.fire(row, col)

    def print_field(self) -> None:
        grid = [["~"] * 10 for _ in range(10)]
        for (row, col), ship in self.field.items():
            for deck in ship.decks:
                if deck.row == row and deck.column == col:
                    if ship.is_drowned:
                        grid[row][col] = "x"
                    elif not deck.is_alive:
                        grid[row][col] = "*"
                    else:
                        grid[row][col] = u"\u25A1"
        for row in grid:
            print("\t".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Ships must be exactly 10.")

        ship_sizes = defaultdict(int)
        occupied = set()

        for ship in self.ships:
            ship_sizes[len(ship.decks)] += 1

            for deck in ship.decks:
                for direction_row in [-1, 0, 1]:
                    for direction_column in [-1, 0, 1]:
                        near_row, near_colum = \
                            (
                                deck.row + direction_row,
                                deck.column + direction_column
                            )
                        if (
                            (near_row, near_colum) in occupied
                            and (near_row, near_colum) not in
                            [
                                (temp_deck.row, temp_deck.column)
                                for temp_deck in ship.decks
                            ]
                        ):
                            raise ValueError(
                                f"Ships are too close to each other at: "
                                f"({near_row}, {near_colum})."
                            )
            for deck in ship.decks:
                occupied.add((deck.row, deck.column))

        if (
            ship_sizes[1] != 4
            and ship_sizes[2] != 3
            and ship_sizes[3] != 2
            and ship_sizes[4] != 1
        ):
            raise ValueError("Wrong number of ships by sizes.")
