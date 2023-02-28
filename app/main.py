from typing import List, Optional


class ValidateFieldError(Exception):
    pass


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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        start_row, start_column = self.start
        end_row, end_column = self.end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(start_row, column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, start_column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        if deck.is_alive:
            deck.is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: List[tuple[int]] = None) -> None:
        self._ships = [Ship(*ship) for ship in ships]
        self._field = {
            tuple((deck.row, deck.column)
                  for deck in ship.decks): ship
            for ship in self._ships
        }
        self._validate_field(self._field)
        self._ocean_map = [["🌊" for _ in range(10)] for _ in range(10)]

    def fire(self, location: tuple[int]) -> str:
        row, col = location
        for ship_location, ship in self._field.items():
            if location in ship_location:
                return ship.fire(row, col)
        self._ocean_map[row][col] = "💨"
        return "Miss!"

    @staticmethod
    def _validate_field(ships: dict[tuple, Ship] = None) -> None:

        text_error = ""
        if len(ships) != 10:
            text_error += f"You don't have enough {10 - len(ships)} ships\n"
        quantity_decks = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in ships.values():
            quantity_decks[len(ship.decks)] += 1

        num = 4
        for decks, quantity in quantity_decks.items():
            if quantity != num:
                text_error += (
                    f"You need to have {decks}-deck ships: {num},"
                    f" but you have: {quantity}\n"
                )
            num -= 1

        for current_ship in ships.values():
            for current_deck in current_ship.decks:
                current_row, current_col = (
                    current_deck.row,
                    current_deck.column
                )
                for other_ship in ships.values():
                    if other_ship != current_ship:
                        for other_deck in other_ship.decks:
                            other_row, other_col = (
                                other_deck.row,
                                other_deck.column
                            )
                            if (abs(current_row - other_row) <= 1
                                    and abs(current_col - other_col) <= 1):
                                text_error += (
                                    "There are ships too "
                                    "close to each other.\n"
                                )

        if text_error:
            raise ValidateFieldError(text_error)

    def _print_map(self, status_map: str) -> None:
        for ship in self._ships:
            for deck in ship.decks:
                row, col = deck.row, deck.column
                if deck.is_alive:
                    self._ocean_map[row][col] = status_map
                else:
                    self._ocean_map[row][col] = "💥"
            if ship.is_drowned:
                for deck in ship.decks:
                    row, col = deck.row, deck.column
                    self._ocean_map[row][col] = "❌"

        # Print the matrix
        for row in self._ocean_map:
            print("".join(row))

    def print_public_map(self) -> None:
        self._print_map("🟥")

    def print_hidden_map(self) -> None:
        self._print_map("🌊")
