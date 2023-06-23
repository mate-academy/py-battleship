from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"{(self.row, self.column)}"


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = self.__set_decks(start, end)
        self.is_drowned = is_drowned

    def __set_decks(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> List[Deck]:
        (x1, y1), (x2, y2) = start, end

        if self.__is_horizontal(x1, x2):
            return self.__horizontal_decks(y1, y2, x1)
        return self.__vertical_decks(x1, x2, y1)

    @staticmethod
    def __horizontal_decks(
            start_column: int,
            end_column: int,
            row: int
    ) -> List[Deck]:
        return [
            Deck(row, column)
            for column in range(start_column, end_column + 1)
        ]

    @staticmethod
    def __vertical_decks(
            start_row: int,
            end_row: int,
            column: int
    ) -> List[Deck]:
        return [Deck(row, column) for row in range(start_row, end_row + 1)]

    @staticmethod
    def __is_horizontal(x1: int, x2: int) -> bool:
        return x1 == x2

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)

        if deck:
            deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int]]]) -> None:
        self.field = self.__set_fields(ships)

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.fire(*location):
                return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    @staticmethod
    def __set_fields(ships: List[Tuple[Tuple[int, int]]]) -> dict:
        return {ship: Ship(*ship) for ship in ships}
