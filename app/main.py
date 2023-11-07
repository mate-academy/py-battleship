from __future__ import annotations
from typing import List


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_position(self) -> tuple[int, int]:
        return self.row, self.column


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self._validate_ship_vector(start, end)

        self.decks = []
        for i in range(end[0] - start[0] + 1):                    # noqa VNE001
            for j in range(end[1] - start[1] + 1):                # noqa VNE001
                self.decks.append(Deck(start[0] + i, start[1] + j))

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.get_position() == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        target = self.get_deck(row, column)
        target.is_alive = False

        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True
        return self.is_drowned

    @staticmethod
    def _validate_ship_vector(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        ship_vector = (end[0] - start[0], end[1] - start[1])
        if 0 not in ship_vector:
            raise ValueError("Ship is not horizontal or vertical.")
        if not 0 <= max(ship_vector) - min(ship_vector) < 5:
            raise ValueError("Wrong length of the ship!")


class Battleship:
    _size = 10
    _symbols = {"empty": "~",
                "alive": u"\u25A1",
                "damaged": "*",
                "out": "x"}

    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}

        for ship_coordinates in ships:
            ship = Ship(ship_coordinates[0], ship_coordinates[1])
            for deck in ship.decks:
                self.field[deck.get_position()] = ship

        self._validate_input()

    def fire(self, location: tuple) -> str:
        target = self.field.get(location)
        if target is None or not target.get_deck(*location).is_alive:
            return "Miss!"
        if target.fire(*location):
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for i in range(self._size):                               # noqa VNE001
            row = []
            for j in range(self._size):                           # noqa VNE001

                ship = self.field.get((i, j))
                if ship is not None:
                    deck = ship.get_deck(i, j)
                    condition = (deck.is_alive, not ship.is_drowned)

                    if all(condition):
                        row.append(self._symbols["alive"])
                    elif any(condition):
                        row.append(self._symbols["damaged"])
                    else:
                        row.append(self._symbols["out"])
                else:
                    row.append(self._symbols["empty"])

            print(*row, sep="  ")

    def _validate_input(self) -> None:
        ships_list = set(self.field.values())
        if len(ships_list) != 10:
            raise ValueError("Total number of ships must be equal to 10.")

        ships_sizes = [len(ship.decks) for ship in ships_list]
        for size in range(1, 5):
            amount = 5 - size
            if ships_sizes.count(size) != amount:
                raise ValueError(f"There must be {amount} {size}-deck ships.")

        for deck in self.field:
            for i in range(deck[0] - 1, deck[0] + 2):             # noqa VNE001
                for j in range(deck[1] - 1, deck[1] + 2):         # noqa VNE001
                    if not self.field.get((i, j)) in (self.field.get(deck),
                                                      None):
                        raise ValueError("Ships must not be adjacent"
                                         " to each other.")


if __name__ == "__main__":
    ships = [
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
    battleship = Battleship(ships)
    battleship.print_field()

    shots = [
        ((9, 9), "Sunk!"),
        ((0, 4), "Miss!"),
        ((0, 3), "Hit!"),
        ((9, 9), "Miss!"),
        ((0, 2), "Hit!"),
        ((0, 2), "Miss!"),
        ((0, 1), "Hit!"),
        ((0, 0), "Sunk!")
    ]

    for shot, expected in shots:
        result = battleship.fire(shot)
        print(f"Shot on {shot}!", "-" * 12, result)
        assert result == expected, f"Got {result}, {expected} expected."
        battleship.print_field()
