from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_hit(self):
        self.is_alive = False

    @property
    def coords(self) -> tuple[int, int]:
        return self.row, self.column


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        if start[0] > end[0] or start[1] > end[1]:
            raise ValueError(
                f"Invalid ship coordinates: start: {start}, end: {end}. "
                "Neither x nor y coordinate of the end can be less than "
                "the corresponding coordinate of the start."
            )

        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        return next(
            (deck for deck in self.decks if deck.coords == (row, column)), None
        )

    def fire(self, row: int, column: int) -> bool:
        self.get_deck(row, column).get_hit()
        return self._check_drowned()

    @property
    def size(self):
        return len(self.decks)

    def _check_drowned(self) -> bool:
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True

        return self.is_drowned


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],  # Wow.
        field_size: tuple[int, int] = (10, 10),
        ship_sizes: tuple[int] = (4, 3, 2, 1),
    ) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {
            deck.coords: ship for ship in self.ships for deck in ship.decks
        }
        self.field_height, self.field_width = field_size

        # Required amounts of ships by size.
        self.ship_sizes = dict([*enumerate(ship_sizes, 1)])

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        return "Sunk!" if self.field[location].fire(*location) else "Hit!"

    def print_field(self):
        for row in range(self.field_height):
            row_cells = []
            for column in range(self.field_width):
                cell = (row, column)
                if cell not in self.field:
                    row_cells.append("~")
                elif (ship := self.field[cell]).is_drowned:
                    row_cells.append("☓")
                else:
                    row_cells.append(
                        "□" if ship.get_deck(*cell).is_alive else "⊠"
                    )
            print(*row_cells, sep="  ")

    def _validate_field(self) -> None:
        if any(
            not 0 <= deck[0] < self.field_height
            or not 0 <= deck[1] < self.field_width
            for deck in self.field
        ):
            raise ValueError("Some of the ships have invalid coordinates.")

        if len(self.ships) != sum(self.ship_sizes.values()):
            raise ValueError("Incorrect number of ships.")

        if self._count_ships() != self.ship_sizes:
            raise ValueError("Incorrect ship sizes.")

        # Definitely refactorable.
        # Unfortunately, I'm not in the mood right now...
        coords = list(self.field.keys())
        for i, coord in enumerate(coords[:-1], 1):
            for other_coord in coords[i:]:
                if (
                    self.field[coord] is not self.field[other_coord]
                    and abs(coord[0] - other_coord[0]) < 2
                    and abs(coord[1] - other_coord[1]) < 2
                ):
                    raise ValueError(
                        "Ships cannot overlap or be "
                        "placed in neighboring cells"
                    )

    def _count_ships(self) -> dict:
        ship_counter = {}

        for ship in self.ships:
            if ship.size in ship_counter:
                ship_counter[ship.size] += 1
            else:
                ship_counter[ship.size] = 1

        return ship_counter
