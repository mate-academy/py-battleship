from collections import Counter


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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                deck = Deck(start_row, column)
                self.decks.append(deck)

        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                deck = Deck(row, start_column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def _are_all_decks_destroyed(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if self._are_all_decks_destroyed():
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[
                tuple[
                    tuple[int, int],
                    tuple[int, int],
                ]
            ],
    ) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        if not self._validate_field():
            raise ValueError("Invalid field")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""

            for column in range(10):
                location = (row, column)

                if location not in self.field:
                    line += "~"

                else:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)

                    if ship.is_drowned:
                        line += "x"
                    elif deck.is_alive:
                        line += "□"
                    else:
                        line += "*"

            print(line)

    def _validate_field(self) -> bool:
        if len(self.ships) != 10:
            return False

        ships_sizes = Counter(len(ship.decks) for ship in self.ships)

        if ships_sizes != {1: 4, 2: 3, 3: 2, 4: 1}:
            return False

        for ship in self.ships:
            for deck in ship.decks:
                for row_shift in (-1, 0, 1):
                    for column_shift in (-1, 0, 1):
                        if row_shift == 0 and column_shift == 0:
                            continue

                        neighbor = (
                            deck.row + row_shift,
                            deck.column + column_shift,
                        )

                        if (
                                neighbor in self.field
                                and self.field[neighbor] is not ship
                        ):
                            return False

        return True
