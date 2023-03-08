from __future__ import annotations

from dataclasses import dataclass


class CountShipsException(Exception):
    pass


class CountFourDecksShipException(Exception):
    pass


class CountThreeDecksShipException(Exception):
    pass


class CountTwoDecksShipException(Exception):
    pass


class CountOneDeckShipException(Exception):
    pass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


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
        self.decks = [Deck(row, column)
                      for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]
        self.live_decks = len(self.decks)

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return True
        return False

    def get_status(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if self.get_deck(row, column) and deck.is_alive:
                return True
        return False


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.ships.values():
            for deck in ship.decks:
                if (deck.row, deck.column) == location:
                    deck.is_alive = False
                    ship.live_decks -= 1
                    if ship.live_decks == 0:
                        ship.is_drowned = True
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"

    def draw_matrix(self, rows: int, columns: int) -> str:
        result = ""

        for column in range(columns):
            for row in range(rows):
                if self.check_deck_status(row, column) == "ship_sunk":
                    result += "x\t"
                elif self.check_deck_status(row, column) == "is_alive":
                    result += u"\u25A1\t"
                elif self.check_deck_status(row, column) == "dead_deck":
                    result += "*\t"
                else:
                    result += "~\t"
            result += "\n"
        return result

    def check_deck_status(self, row: int, column: int) -> bool | str:
        for ship in self.ships.values():
            if ship.get_deck(row, column):
                if ship.live_decks == 0:
                    return "ship_sunk"
                if ship.get_status(row, column):
                    return "is_alive"
                return "dead_deck"
        return False

    def _validate_field(self) -> bool:
        if len(self.ships) != 10:
            raise CountShipsException

        ship_on_the_board = [len(ship.decks) for ship in self.ships.values()]

        if 4 not in ship_on_the_board or ship_on_the_board.count(4) != 1:
            raise CountFourDecksShipException

        if 3 not in ship_on_the_board or ship_on_the_board.count(3) != 2:
            raise CountThreeDecksShipException

        if 2 not in ship_on_the_board or ship_on_the_board.count(2) != 3:
            raise CountTwoDecksShipException

        if 1 not in ship_on_the_board or ship_on_the_board.count(1) != 4:
            raise CountOneDeckShipException

        return True
