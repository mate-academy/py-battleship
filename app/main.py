from typing import Any


class ShipCountError(Exception):
    pass


Coords = tuple[int, int]


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = False,
        appearance: str = "~",
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.appearance = appearance


class Ship:
    def __init__(
        self,
        start: Coords,
        end: Coords,
        is_drowned: bool = False
    ) -> None:
        self.length = 0
        self.decks = []
        self.create_from_tuples_list(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, coords: Coords) -> Deck:
        for deck in self.decks:
            if tuple([deck.row, deck.column]) == coords:
                return deck

    def sunk(self) -> None:
        for deck in self.decks:
            deck.appearance = "x"

    def fire(self, coords: Coords) -> str:
        deck = self.get_deck(coords)
        deck.is_alive = False
        deck.appearance = "*"
        self.length -= 1
        if self.length != 0:
            return "Hit!"
        self.sunk()
        return "Sunk!"

    def create_from_tuples_list(
        self, start: Coords, end: Coords
    ) -> None:
        x1, y1 = start
        x2, y2 = end
        length = max(abs(x2 - x1), abs(y2 - y1)) + 1
        for i in range(length):
            self.length += 1
            if x1 == x2:
                self.decks.append(
                    Deck(x1, y1 + i, is_alive=True, appearance="\u25A1")
                )
            elif y1 == y2:
                self.decks.append(
                    Deck(x1 + i, y1, is_alive=True, appearance="\u25A1")
                )


class Battleship:
    def __init__(
        self, ships: list[tuple[Coords, Coords]]
    ) -> None:
        self._map = [[Deck(i, j) for j in range(10)] for i in range(10)]
        self.field = self._create_ships(ships)

    def _validate_field(self) -> None:
        ships = list(self.field.values())
        expected_counts = {0: 10, 1: 4, 2: 3, 3: 2, 4: 1}
        counts = {i: sum(len(ship.decks) == i for ship in ships) for i in range(5)}
        for i in range(5):
            if counts[i] == expected_counts[i]:
                raise ShipCountError(
                    f"There should be {expected_counts[i]} {i}-deck ships"
                )
        for ship in ships:
            for deck in ship.decks:
                row, col = deck.row, deck.column
                neighbors = [
                    (row + i, col + j)
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if (0 <= row + i < 10)
                    and (0 <= col + j < 10)
                    and (i != 0 or j != 0)
                ]
                if any(neighbor in self.field for neighbor in neighbors):
                    raise ValueError(
                        "Ships should not be located in neighboring cells"
                    )

    def fire(self, location: tuple) -> str | None:
        if location not in self.field:
            return "Miss!"
        return self.field[location].fire(location)

    @staticmethod
    def _create_ships(
        ships: list[tuple[Coords, Coords]]
    ) -> dict[tuple[Any, ...], Ship]:
        field = dict()
        ships = [Ship(*coords) for coords in ships]
        for ship in ships:
            for deck in ship.decks:
                field[tuple([deck.row, deck.column])] = ship
        return field

    def print_field(self) -> None:
        for ind_row, row in enumerate(self._map):
            for ind_column, deck in enumerate(row):
                coords = (
                    ind_row,
                    ind_column,
                )
                if coords not in self.field:
                    print(" ", deck.appearance, end="  ")
                if coords in self.field:
                    print(
                        " ",
                        self.field[coords].get_deck(coords).appearance,
                        end="  ",
                    )
            print()
