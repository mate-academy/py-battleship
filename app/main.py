from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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

        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for column in range(
                min(start_column, end_column),
                max(start_column, end_column) + 1
            ):
                self.decks.append(
                    Deck(start_row, column)
                )
        else:
            for row in range(
                min(start_row, end_row),
                max(start_row, end_row) + 1
            ):
                self.decks.append(
                    Deck(row, start_column)
                )

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        if deck and deck.is_alive:
            deck.is_alive = False

        self.is_drowned = all(not deck.is_alive for deck in self.decks)

    def get_length(self) -> Any:
        return len(self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}

        for start_coordinate, end_coordinate in ships:
            ship = Ship(start_coordinate, end_coordinate)
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location

        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = []

            for column in range(10):
                location = (row, column)
                if location not in self.field:
                    line.append("~")
                    continue

                ship = self.field[location]
                deck = ship.get_deck(row, column)
                if ship.is_drowned:
                    line.append("x")
                elif deck.is_alive:
                    line.append(u"\u25A1")
                else:
                    line.append("*")

            print(" ".join(line))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships")

        ship_lengths = [ship.get_length() for ship in self.ships]

        if ship_lengths.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships")

        if ship_lengths.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships")

        if ship_lengths.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships")

        if ship_lengths.count(4) != 1:
            raise ValueError("There should be 1 four-deck ship")

        occupied = {}

        for ship in self.ships:
            for deck in ship.decks:
                row = deck.row
                column = deck.column

                for delta_row in range(-1, 2):
                    for delta_column in range(-1, 2):
                        neighbor = (
                            row + delta_row,
                            column + delta_column
                        )

                        if (
                            neighbor in occupied
                            and occupied[neighbor] is not ship
                        ):
                            raise ValueError(
                                "Ships cannot touch each other"
                            )

                occupied[(row, column)] = ship
