from math import dist
from collections import Counter


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

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column})"

    def __str__(self) -> str:
        return self.__repr__()


class Ship:
    MAX_SHIP_LENGTH: int = 4

    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.length = int(dist(start, end)) + 1
        if self.length > self.MAX_SHIP_LENGTH:
            raise ValueError(
                "Max length for ship "
                f"it {self.MAX_SHIP_LENGTH}, not {self.length}"
            )

        self.decks: list[Deck] = []
        self._create_decks(start, end)
        self.is_drowned = is_drowned
        self._alive_decks = self.length

    def _create_decks(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        # there it is necessary to avoid ZeroDivisionError
        distance = self.length - 1 if self.length != 1 else 1
        vector = (  # direction vector (unit vector)
            (end[0] - start[0]) // distance,
            (end[1] - start[1]) // distance
        )
        self.decks = [
            Deck(
                start[0] + (vector[0] * i),
                start[1] + (vector[1] * i)
            ) for i in range(0, self.length)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        raise ValueError(f"Deck ({row}, {column}) is not present in this ship")

    def fire(self, row: int, column: int) -> bool:
        """returns True if the ship sank after this shot"""
        deck = self.get_deck(row, column)
        if not deck.is_alive:
            raise ValueError(f"Deck ({row}, {column}) is already death")

        deck.is_alive = False
        self._alive_decks -= 1
        if not self._alive_decks:
            self.is_drowned = True
        return self.is_drowned


class Battleship:
    SHIPS_COUNT = 10
    DEFAULT_SIZES = [(1, 4), (2, 3), (3, 2), (4, 1)]
    DIRECTIONS = (
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    )
    MAX_ROWS = 10
    MAX_COLUMNS = 10

    def __init__(self, ships: list[tuple]) -> None:
        self.field = ships

    def _is_valid_coord(self, row: int, column: int) -> bool:
        return (
            (0 <= row < self.MAX_ROWS)
            and (0 <= column < self.MAX_COLUMNS)
        )

    @property
    def field(self) -> dict[tuple, Ship]:
        return self._field

    @field.setter
    def field(self, ships: list[tuple]) -> None:
        self._field: dict[tuple, Ship] = {}
        self._create_fields(ships)
        self._validate_field(ships)

    def _create_fields(self, ships: list[tuple]) -> None:
        for ship_info in ships:
            ship = Ship(*ship_info)
            for deck in ship.decks:
                coords = deck.row, deck.column
                if coords in self._field:
                    raise ValueError(
                        f"This cell ({coords[0]}, {coords[1]}) is "
                        "already occupied"
                    )
                self._field[coords] = ship

    def _validate_field(self, ships: list[tuple]) -> None:
        # the total number of the ships should be SHIP_COUNT
        if len(ships) != self.SHIPS_COUNT:
            raise ValueError(
                "The number of ships must "
                "be exactly {self.SHIPS_COUNT}"
            )

        # ships shouldn't be located in the neighboring cells
        # (even if cells are neighbors by diagonal)
        for coords, ship in self._field.items():
            for direction in self.DIRECTIONS:
                new_coords = (
                    coords[0] + direction[0],
                    coords[1] + direction[1]
                )
                if not self._is_valid_coord(*new_coords):
                    continue
                if (
                    new_coords in self._field
                    and self._field[new_coords] != ship
                ):
                    raise ValueError("Is not valid place for ship")

        # validation of the correct number of ships of all sizes
        freq = Counter(self._field[start].length for start, _ in ships)
        if self.DEFAULT_SIZES != sorted(list(freq.items())):
            raise ValueError("Wrong ships count")

    def fire(self, location: tuple) -> str:
        if ship := self._field.get(location):
            if ship.fire(*location):
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        lines = []
        for row in range(self.MAX_ROWS):
            line = []
            for column in range(self.MAX_COLUMNS):
                location = row, column
                if ship := self._field.get(location):
                    if ship.is_drowned:
                        line.append("x")
                    elif ship.get_deck(*location).is_alive:
                        line.append("□")
                    else:
                        line.append("*")
                else:
                    line.append("~")
            lines.append(line)
        return "\n".join("   ".join(line) for line in lines)

    def __str__(self) -> str:
        return self.__repr__()
