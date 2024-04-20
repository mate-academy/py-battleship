from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name
        self.protected_name = f"_{name}"

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: Any, value: Any) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Cooradinate(Validator):

    def __init__(self, min_value: int = 0, max_value: int = 9) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Coordinate should be integer")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                (
                    f"Coordinate should not be less than "
                    f"{self.min_value} and not greater than {self.max_value}"
                )
            )


class Deck:

    row = Cooradinate()
    column = Cooradinate()

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck: ({self.row}, {self.column}, is_alive={self.is_alive})"

    def __eq__(self, other: object) -> bool:
        return self.row == other.row and self.column == other.column


class Ship:

    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        self.decks: list = [Deck]
        self._set_decks(start, end)
        self.is_drowned = is_drowned
        self.alive_decks = len(self.decks)

    def _set_decks(self, start: tuple, end: tuple) -> None:
        if start[0] > end[0] or start[1] > end[1]:
            start, end = end, start
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        elif start[1] == end[1]:
            self.decks = [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            self.alive_decks -= 1

        if self.alive_decks == 0:
            self.is_drowned = True

    def __repr__(self) -> str:
        return f"Ship({len(self)} deck's ship)"

    def __len__(self) -> int:
        return len(self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if self.field.get(location) is None:
            return "Miss!"
        ship = self.field.get(location)
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if self.field.get((row, column)) is None:
                    print("~", end="  ")
                else:
                    ship = self.field.get((row, column))
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        print("□", end="  ")
                    elif not deck.is_alive and not ship.is_drowned:
                        print("*", end="  ")
                    elif not deck.is_alive and ship.is_drowned:
                        print("x", end="  ")
            print()

    @staticmethod
    def is_neighbour_location(location_1: tuple, location_2: tuple) -> bool:
        x_1, y_1 = location_1
        x_2, y_2 = location_2
        return abs(x_1 - x_2) <= 1 and abs(y_1 - y_2) <= 1

    def _validate_field(self) -> None:
        if len(self.field) != 20:
            raise
        requirments = {1: 4, 2: 3, 3: 2, 4: 1}
        ships_count = {}
        for ship in self.ships:
            length = len(ship)
            ships_count[length] = ships_count.get(length, 0) + 1
        if requirments != ships_count:
            raise
        for coordinates, ship in self.field.items():
            for other_coord, other_ship in self.field.items():
                if (
                    Battleship.is_neighbour_location(coordinates, other_coord)
                    and ship is not other_ship
                ):
                    raise
