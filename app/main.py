import dataclasses
from typing import Union


class ErrorTotalNumberShips(Exception):
    pass


class ErrorNumberDecks(Exception):
    pass


class ErrorNeighboringCells(Exception):
    pass


class ErrorNotOneLineShips(Exception):
    pass


@dataclasses.dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        """Create decks and save them to a list `self.decks`"""
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        """Change the `is_alive` status of the deck
        And update the `is_drowned` value if it's needed"""
        is_alive_ls = []
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
            is_alive_ls.append(not deck.is_alive)
        self.is_drowned = all(is_alive_ls)
        return "Sunk!" if self.is_drowned is True else "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        """Create a dict `self.field`.
        Its keys are tuples - the coordinates of the non-empty cells,
        A value for each cell is a reference to the ship
        which is located in it"""
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ErrorTotalNumberShips(
                "The total number of the ships should be 10"
            )
        decks_dict = {}
        decks_count_ls = [0, 0, 0, 0]
        for coordinates, ship in self.field.items():
            if coordinates[0][0] != coordinates[1][0] \
                    and coordinates[0][1] != coordinates[1][1]:
                raise ErrorNotOneLineShips("Ships must be in one line")

            decks_count = len(ship.decks) - 1
            try:
                decks_count_ls[decks_count] += 1
            except IndexError:
                raise ErrorNumberDecks("Number of decks can`t be more than 4")

            for deck in ship.decks:
                decks_dict[(deck.row, deck.column)] = ship

        words = ["single", "double", "three", "four"]
        for index, decks_count in enumerate(decks_count_ls):
            if decks_count != (4 - index):
                raise ErrorNumberDecks(
                    f"There should be {4 - index} {words[index]}-deck ships"
                )

        for coordinates, ship in decks_dict.items():
            row, column = coordinates
            for row_offset in range(-1, 2, 2):
                for column_offset in range(-1, 2, 2):
                    another_ship = decks_dict.get(
                        (row + row_offset, column + column_offset)
                    )
                    if another_ship != ship and another_ship is not None:
                        raise ErrorNeighboringCells(
                            "Ships shouldn't be located in the neighboring "
                            "cells (even if cells are neighbors by diagonal) "
                            f"cell ("
                            f"{(row + row_offset, column + column_offset)}"
                            f") should be free"
                        )

    def fire(self, location: tuple) -> str:
        """This function should check whether the location
        is a key in the `self.field`
        If it is, then it should check if this cell is the last alive
        in the ship or not."""
        result = "Miss!"
        for coordinates, ship in self.field.items():
            if coordinates[0][0] <= location[0] <= coordinates[1][0] \
                    and coordinates[0][1] <= location[1] <= coordinates[1][1]:
                result = ship.fire(location[0], location[1])
                break
        return result

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]

        for coord, ship in self.field.items():
            for row in range(coord[0][0], coord[1][0] + 1):
                for col in range(coord[0][1], coord[1][1] + 1):
                    symbol = u"\u25A1"
                    deck = ship.get_deck(row, col)
                    if deck is not None and deck.is_alive is False:
                        symbol = "*"
                        if ship.is_drowned:
                            symbol = "x"

                    field[row][col] = symbol
        for row in range(10):
            print("     ".join(field[row]) + "\n")
