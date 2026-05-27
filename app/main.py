class InvalidFireMove(Exception):
    pass


class NotExistingDeckError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self._row = row
        self._column = column
        self._is_alive = is_alive

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        if not self._is_alive:
            raise InvalidFireMove("A deck is already fired")

        self._is_alive = value


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        try:
            if start[0] == end[0]:  # horizontal ship
                self._decks = [
                    Deck(start[0], column)
                    for column in range(start[1], end[1] + 1)
                ]
            elif start[1] == end[1]:  # vertical ship
                self._decks = [
                    Deck(row, start[1])
                    for row in range(start[0], end[0] + 1)
                ]
            else:
                raise ValueError("Invalid ship was provided")
            self._is_drowned = is_drowned
        except IndexError as exc:
            raise ValueError("Invalid ship coordinates was provided") from exc

    @property
    def decks(self) -> list:
        return self._decks

    @property
    def is_drowned(self) -> bool:
        return self._is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise NotExistingDeckError(
            f"Deck with row={row}, column={column} was not found"
        )

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        self._is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self._field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                coords = (deck.row, deck.column)

                if coords in self._field:
                    raise ValueError(f"Ships overlap at {coords}")
                self._field[coords] = ship

        self._validate_fields()

    @property
    def field(self) -> dict[tuple[int, int], Ship]:
        return self._field

    def fire(self, location: tuple[int, int]) -> str:
        if not isinstance(location, tuple) or len(location) != 2:
            raise ValueError("Location must be (row, column)")

        ship = self.field.get(location)

        if not ship:
            return "Miss!"

        row, column = location
        try:
            ship.fire(row, column)
        except InvalidFireMove:
            return "Already hit deck!"

        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        if not self.field:
            print("Empty field")
            return

        for row in range(10):
            for column in range(10):
                coords = (row, column)
                ship = self.field.get(coords)

                if ship is None:
                    print("~", end="")
                elif ship.is_drowned:
                    print("x", end="")
                else:
                    deck = ship.get_deck(row, column)
                    print("□" if deck.is_alive else "*", end="")

                print(end="  ")
            print()

    def _validate_fields(self) -> None:
        if len(self.field) != 20:
            raise ValueError(
                "The total number of the ships should be "
                "10, 1 - xxxx, 2 - xxx, 3 - xx, 4 - x"
            )
        if self._count_ship(dimensions=1) != 4:
            raise ValueError(
                "The total number of the singe-deck ships should be 4"
            )
        if self._count_ship(dimensions=2) != 3:
            raise ValueError(
                "The total number of the double-deck ships should be 3"
            )
        if self._count_ship(dimensions=3) != 2:
            raise ValueError(
                "The total number of the three-deck ships should be 2"
            )
        if self._count_ship(dimensions=4) != 1:
            raise ValueError(
                "The total number of the four-deck ships should be 1"
            )
        if self._is_placement_invalid():
            raise ValueError(
                "The ship placement is invalid you need to keep "
                "gap in 1 deck between your ships"
            )

    def _count_ship(self, dimensions: int) -> int:
        ships = {ship for ship in self.field.values()}
        return sum(1 for ship in ships if len(ship.decks) == dimensions)

    def _is_placement_invalid(self) -> bool:
        for coords, ship in self.field.items():
            row, column = coords
            for dx in [0, 1, -1]:
                for dy in [0, 1, -1]:
                    coords = (row + dx, column + dy)
                    if coords in self.field and self.field[coords] != ship:
                        return True
        return False


battle_ship = Battleship(
    ships=[
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
)

battle_ship.print_field()
