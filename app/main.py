from collections import Counter
from typing import TypeAlias


Coordinate: TypeAlias = tuple[int, int]
ShipData: TypeAlias = tuple[Coordinate, Coordinate]
ShipsData: TypeAlias = list[ShipData]


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Coordinate,
            end: Coordinate,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        self.start_row = min(start[0], end[0])
        self.start_column = min(start[1], end[1])

        self.end_row = max(start[0], end[0])
        self.end_column = max(start[1], end[1])

        for row in range(self.start_row, self.end_row + 1):
            for column in range(self.start_column, self.end_column + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)

        if deck is None or not deck.is_alive:
            return False

        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return True


class Battleship:
    def __init__(self, ships: ShipsData) -> None:
        self.field: dict[tuple, Ship] = {}

        if not self._validate_field(ships):
            raise ValueError("Invalid ships configuration")

        for ship_positions in ships:
            self.field[ship_positions] = (
                Ship(ship_positions[0], ship_positions[1])
            )

    def fire(self, location: tuple) -> str:

        row, column = location

        for ship in self.field.values():
            deck = ship.get_deck(row, column)
            if deck and deck.is_alive:
                is_drowned = ship.fire(row, column)
                if is_drowned:
                    return "Sunk!"

                return "Hit!"

        return "Miss!"

    def game_board(self) -> None:
        board: list[list[str]] = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    board[deck.row][deck.column] = "x"
                elif deck.is_alive:
                    board[deck.row][deck.column] = "\u25A1"
                else:
                    board[deck.row][deck.column] = "*"

        for row in board:
            print(" ".join(row))

    def _validate_field(self, ships: ShipsData) -> bool:
        if len(ships) != 10:
            raise ValueError("Invalid number of ships. Expected 10 ships.")
        elif not self._validate_decks_count(ships):
            raise ValueError(
                "Invalid fleet composition. "
                "Expected 4 single-deck, 3 double-deck, "
                "2 triple-deck and 1 four-deck ships."
            )
        elif not self._validate_ship_neighbors(ships):
            raise ValueError("Ships cannot touch each other, even diagonally.")

        return True

    @staticmethod
    def _validate_decks_count(ships: ShipsData) -> bool:
        decks_ship: list[int] = []
        expected_ships = {1: 4, 2: 3, 3: 2, 4: 1}

        for ship in ships:
            decks_sum: int = 0
            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    decks_sum += 1
            decks_ship.append(decks_sum)

        if Counter(decks_ship) != expected_ships:
            return False

        return True

    @staticmethod
    def _validate_ship_neighbors(ships: ShipsData) -> bool:
        occupied_cells = set()

        for ship in ships:
            (start_row, start_column), (end_row, end_column) = ship

            ship_cells = set()

            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    ship_cells.add((row, column))

            for row, column in ship_cells:
                for row_offset in (-1, 0, 1):
                    for column_offset in (-1, 0, 1):

                        neighbor = (row + row_offset, column + column_offset)

                        if neighbor in occupied_cells:
                            return False

            occupied_cells.update(ship_cells)

        return True
