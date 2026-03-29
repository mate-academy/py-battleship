from collections import Counter
from dataclasses import dataclass
from typing import TypeAlias, Iterable


Coord: TypeAlias = tuple[int, int]


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class InvalidCoordsException(Exception):
    pass


class Ship:
    def __init__(
        self, start: Coord, end: Coord, is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned

        self.decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column, not is_drowned))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1], not is_drowned))
        else:
            raise InvalidCoordsException(
                "coords passed to Ship() are not valid"
            )

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return True
        return False


class InvalidFieldException(Exception):
    pass


class Battleship:
    FIELD_SIZE = 10

    def __init__(self, ships: Iterable[tuple[Coord, Coord]]) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                coord = (deck.row, deck.column)
                if coord in self.field:
                    raise InvalidFieldException(
                        f"cell {coord} is already taken"
                    )
                self.field[coord] = ship

        self._validate_field()

    def fire(self, location: Coord) -> str:
        if location not in self.field:
            return "Miss!"
        if self.field[location].fire(*location):
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(self.FIELD_SIZE):
            for column in range(self.FIELD_SIZE):
                coords = (row, column)
                if coords not in self.field:
                    print("~", end=" ")
                    continue
                ship = self.field[coords]
                if ship.is_drowned:
                    print("x", end=" ")
                elif ship.get_deck(row, column).is_alive:
                    print("\u25A1", end=" ")
                else:
                    print("*", end=" ")
            print()

    def _validate_field(self) -> None:
        self._validate_ship_count()
        self._validate_ship_positions()

    def _validate_ship_count(self) -> None:
        ships = set(self.field.values())
        if len(ships) != 10:
            raise InvalidFieldException(
                "the total number of the ships should be 10"
            )
        counter = Counter(len(ship.decks) for ship in ships)
        for size, expected_count, verbose_name in (
            (1, 4, "single"),
            (2, 3, "double"),
            (3, 2, "three"),
            (4, 1, "four"),
        ):
            if counter[size] != expected_count:
                raise InvalidFieldException(
                    f"there should be {expected_count} {verbose_name}-deck"
                    " ship" + ("s" if expected_count != 1 else "")
                )

    def _validate_ship_positions(self) -> None:
        for row, column in self.field:
            current_ship = self.field[(row, column)]
            # check nearby cells
            for row_adj in range(-1, 2):
                for column_adj in range(-1, 2):
                    coord = (row + row_adj, column + column_adj)
                    if (
                        coord in self.field
                        and self.field[coord] is not current_ship
                    ):
                        raise InvalidFieldException(
                            "ships shouldn't be located in the"
                            " neighboring cells"
                        )
