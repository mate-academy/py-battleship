import dataclasses
from typing import Callable
from string import ascii_uppercase
from collections import namedtuple


class ValidationError(Exception):
    pass


@dataclasses.dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = {(row, column): Deck(row, column)
                      for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)
                      }

    def get_deck(self, row: int, column: int) -> Callable:
        return self.fire(self.decks.get((row, column)))

    def fire(self, deck: Deck) -> str:
        deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks.values()):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = {coordinates: Ship(*coordinates) for coordinates in ships}
        self.field = self.create_field(ships)
        self._validate_field(self.ships)

    def fire(self, location: tuple) -> str:
        for coordinates, ship in self.ships.items():
            if coordinates[0] <= location <= coordinates[1]:
                result = ship.get_deck(*location)
                self.mark_the_hit_and_print_field(location, ship, result)
                return result
        self.mark_the_hit_and_print_field(location)
        return "Miss!"

    def mark_the_hit_and_print_field(self,
                                     location: tuple,
                                     ship: Ship = None,
                                     result: str = None) -> None:
        row, col = location
        if result == "Hit!":
            self.field[row][col] = "*"
        elif result == "Sunk!":
            self.__loop_to_fill_field(ship, self.field, "X")

        print(f"    {' '.join(ascii_uppercase[:10])}")
        print("\u2014 " * 12)
        for index, row in enumerate(self.field):
            print(f"{index} | {' '.join(row)}")

    def create_field(self, battle_ships: list) -> list:
        field = [["~"] * 10 for _ in range(10)]
        ship_namedtuple = namedtuple("Ship", ["start", "end"])

        for ship in battle_ships:
            ship_named = ship_namedtuple(ship[0], ship[1])
            self.__loop_to_fill_field(ship_named, field, u"\u25A1")

        return field

    def _validate_field(self, ships: dict[Ship]) -> None:
        for ship in ships.values():
            for deck in ship.decks.values():
                for row in range(deck.row - 1, deck.row + 2):
                    for col in range(deck.column - 1, deck.column + 2):
                        if 0 <= row <= 9 and 0 <= col <= 9:
                            if (self.field[row][col] == u"\u25A1"
                                    and Deck(row, col)
                                    not in ship.decks.values()):
                                raise ValidationError(
                                    "The field is not correctly compiled")

        count_decks = 4
        count_ships = 1
        for _ in range(4):
            if not sum(len(ship.decks) == count_decks
                       for ship in ships.values()) == count_ships:
                raise ValidationError("The field is not correctly compiled")
            count_decks -= 1
            count_ships += 1

        if len(ships) != 10:
            ValidationError("The field is not correctly compiled")

    @staticmethod
    def __loop_to_fill_field(ship: Ship, field: list, char: str) -> None:
        if ship.start == ship.end:
            field[ship.start[0]][ship.start[1]] = char
        elif ship.start[0] != ship.end[0]:
            for row in range(ship.start[0], ship.end[0] + 1):
                field[row][ship.start[1]] = char
        elif ship.start[1] != ship.end[1]:
            for column in range(ship.start[1], ship.end[1] + 1):
                field[ship.end[0]][column] = char
