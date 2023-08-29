import math
from typing import Tuple, List, Dict, Type

from app.battleship.exception.exception import (
    CloseLocationException,
    WrongShipsNumber
)


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    start: tuple
    end: tuple
    length: int
    is_drowned: bool

    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        diff_row: int = self.start[0] - self.end[0]
        diff_column: int = self.start[1] - self.end[1]
        self.length = int(math.sqrt(diff_row ** 2 + diff_column ** 2) + 1)

        self.decks: List[Deck] = self.__create_decks()

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False

        if not self.is_drowned and sum(
                [deck.is_alive for deck in self.decks]
        ) == 0:
            self.is_drowned = True

    def __create_decks(self) -> List:
        decks: List[Deck] = []
        current_row = self.start[0]
        current_col = self.start[1]
        decks.append(Deck(current_row, current_col))

        while (
                not current_row == self.end[0]
                or not current_col == self.end[1]
        ):
            if (self.end[0] - current_row) > 0:
                current_row += 1

            if (self.end[1] - current_col) > 0:
                current_col += 1

            decks.append(Deck(current_row, current_col))

        return decks

    def __str__(self) -> str:
        return f"Ship[{self.start}, {self.end}]"


class Battleship:
    ROWS: int = 10
    COLUMNS: int = 10

    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[
            Tuple[int, int], Type[Ship]
        ] = self.__create_fields(ships)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field and not self.field[location].is_drowned:
            current_deck = self.field[location].get_deck(
                location[0],
                location[1]
            )
            if current_deck.is_alive:
                self.field[location].fire(location[0], location[1])
                if self.field[location].is_drowned:
                    return "Sunk!"

                return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        battle_field = []
        for row in range(self.ROWS):
            row_fields = []
            for column in range(self.COLUMNS):
                location = (row, column)
                if location in self.field:
                    deck = self.field[location].get_deck(row, column)
                    if self.field[location].is_drowned:
                        row_fields.append("X")
                    elif deck.is_alive:
                        row_fields.append(u"\u25A1")
                    else:
                        row_fields.append("*")
                else:
                    row_fields.append("~")

            battle_field.append("\t".join(row_fields))

        print("\n".join(battle_field))

    @staticmethod
    def __create_fields(
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> dict:
        field_dict = {}
        for row, column in ships:
            ship = Ship(row, column)
            current_row = ship.start[0]
            current_col = ship.start[1]
            field_dict[(current_row, current_col)] = ship
            while (
                    not current_row == ship.end[0]
                    or not current_col == ship.end[1]
            ):
                if (ship.end[0] - current_row) > 0:
                    current_row += 1

                if (ship.end[1] - current_col) > 0:
                    current_col += 1

                field_dict[(current_row, current_col)] = ship

        return field_dict

    def _validate_field(self) -> None:
        for location, ship in self.field.items():
            for neighbor_row in range(location[0] - 1, location[0] + 1):
                for neighbor_col in range(location[1] - 1, location[1] + 1):
                    neighbor_location = (neighbor_row, neighbor_col)
                    if (
                        neighbor_location in self.field
                        and not self.field[neighbor_location] == ship
                    ):
                        raise CloseLocationException(
                            str(ship),
                            str(self.field[neighbor_location])
                        )

        ships: List[Type[Ship]] = list(set(self.field.values()))

        self.__check_ship_count(ships, 10)
        self.__check_ship_count(ships, 4, "single-deck")
        self.__check_ship_count(ships, 3, "double-deck")
        self.__check_ship_count(ships, 2, "three-deck")
        self.__check_ship_count(ships, 1, "four-deck")

    @staticmethod
    def __check_ship_count(
        ships: List[Type[Ship]],
        number: int,
        ship_type: str | None = None
    ) -> None:
        if type:
            if not sum([1 for ship in ships if ship.length == 1]) == 4:
                raise WrongShipsNumber(f"Should be {number} {ship_type} ships")
        else:
            if not len(ships) == 10:
                raise WrongShipsNumber(f"Should be {number} ships")
