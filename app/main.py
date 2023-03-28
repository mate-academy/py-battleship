from typing import Optional

ROWS = 10
COLUMNS = 10


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.coordinates = (row, column)
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}) - alive: {self.is_alive} |"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = self._create_deck(start, end)
        self.is_drowned = is_drowned

    def _create_deck(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[Deck]:
        type_of_ship = self._check_type_of_ship(start, end)
        if type_of_ship == "1-deck-ship":
            return [Deck(*start)]
        if type_of_ship == "horizontal ship":
            return [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        return [
            Deck(row, start[1])
            for row in range(start[0], end[0] + 1)
        ]

    @staticmethod
    def _check_type_of_ship(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> str:
        if start == end:
            return "1-deck-ship"
        if start[0] == end[0]:
            return "horizontal ship"
        return "vertical ship"

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck_fired = self.get_deck(row, column)
        deck_fired.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True

    def __repr__(self) -> str:
        return f"{self.decks}, Drowned: {self.is_drowned} || "


class Battleship:
    def __init__(
            self,
            ships: list[tuple]
    ) -> None:
        ships_list = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in ships_list:
            for deck in ship.decks:
                self.field[deck.coordinates] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(ROWS):
            for column in range(COLUMNS):
                if not (row, column) in self.field:
                    print(" ~ ", end="")
                elif self.field[(row, column)].get_deck(row, column).is_alive:
                    print(u" \u25A1 ", end="")
                else:
                    print(" x ", end="")
            print("")
