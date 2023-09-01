from __future__ import annotations
from typing import List


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            ship: Ship,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.ship = ship

    def is_touching(self, other: Deck) -> bool:
        row_diff = max(self.row, other.row) - min(self.row, other.row)
        column_diff = max(self.column, other.column) - \
            min(self.column, other.column)
        if column_diff == 0 and row_diff == 1:
            return True
        if row_diff == 0 and column_diff == 1:
            return True
        if row_diff == 1 and column_diff == 1:
            return True
        return False

    def __str__(self) -> str:
        if self.is_alive:
            return "\u25A1"
        if self.ship.is_drowned:
            return "x"
        return "*"

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.length = 0
        self.start = start
        self.end = end
        self.decks = self.get_placed()
        self.is_drowned = is_drowned

    def get_placed(self) -> list:
        x_coords = []
        y_coords = []
        if self.start[0] == self.end[0]:
            x_coords = self.start[0]
            for y_ in range(
                    min(self.start[1], self.end[1]),
                    max(self.start[1], self.end[1]) + 1
            ):
                y_coords.append(y_)
                self.length += 1
        if self.start[1] == self.end[1]:
            y_coords = self.start[1]
            for x_ in range(
                    min(self.start[0], self.end[0]),
                    max(self.start[0], self.end[0]) + 1
            ):
                if isinstance(x_coords, list):
                    x_coords.append(x_)
                    self.length += 1
        if x_coords == y_coords or self.length == 1:
            return [Deck(x_coords, y_coords, self)]
        return [
            Deck(x_coords, y_coords[i], self) if isinstance(x_coords, int)
            else Deck(x_coords[i], y_coords, self) for i in range(self.length)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None | bool:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
        if all([deck.is_alive is False for deck in self.decks]):
            self.is_drowned = True
            return True

    def __repr__(self) -> str:
        return f"({self.start}{self.end})"

    def __str__(self) -> str:
        return f"{' '.join([deck.__str__() for deck in self.decks])}"


class Battleship:
    def __init__(
            self,
            ships: List[Ship]
    ) -> None:
        self.field = {deck: deck.ship for deck in self.get_decks(ships)}
        self._validate_field()

    @staticmethod
    def get_decks(ships: List[Ship]) -> list:
        if isinstance(ships[0], tuple):
            ships = [Ship(coords[0], coords[1]) for coords in ships]
        decks_nested = [ship.decks for ship in ships]
        decks = []
        for ls in decks_nested:
            for deck in ls:
                decks.append(deck)
        return decks

    def print_field(self) -> None:
        field = {i: ["~" for _ in range(10)] for i in range(10)}
        for deck in self.field:
            field[deck.row][deck.column] = deck
        for key in field:
            for value in field[key]:
                print(value, end="    ")
            print("\n")

    def fire(self, location: tuple) -> str:
        for deck in self.field:
            if deck.row == location[0] and deck.column == location[1]:
                if deck.ship.fire(deck.row, deck.column):
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        ships_amount = len(set(self.field.values()))
        if ships_amount < 10:
            raise ValidationError(f"Amount of ships must equal 10,"
                                  f" ({ships_amount} found)")
        self._validate_amount()
        self._validate_location()

    def _validate_amount(self) -> None:
        ships_lengthes = {}
        for ship in set(self.field.values()):
            if ship.length in ships_lengthes:
                ships_lengthes[ship.length] += [ship]
            else:
                ships_lengthes[ship.length] = [ship]
        for length in ships_lengthes:
            if not 1 <= length <= 4:
                raise ValidationError(f"Size of a ship must be from 1 to 4,"
                                      f" (found {length})")
        if len(ships_lengthes[1]) != 4:
            raise ValidationError(f"There must be 4 single-deck ships,"
                                  f" ({len(ships_lengthes[1])} found)")
        if len(ships_lengthes[2]) != 3:
            raise ValidationError(f"There must be 3 double-deck ships,"
                                  f" ({len(ships_lengthes[2])} found)")
        if len(ships_lengthes[3]) != 2:
            raise ValidationError(f"There must be 2 three-deck ships,"
                                  f" ({len(ships_lengthes[3])} found)")
        if len(ships_lengthes[4]) != 1:
            raise ValidationError(f"There must be 1 four-deck ship,"
                                  f" ({len(ships_lengthes[4])} found)")

    def _validate_location(self) -> None:
        for deck in self.field:
            for deck1 in self.field:
                if deck.ship == deck1.ship:
                    continue
                if deck.is_touching(deck1):
                    raise ValidationError("Ships must not touch each other,"
                                          " even by diagonal")


class ValidationError(Exception):
    pass
