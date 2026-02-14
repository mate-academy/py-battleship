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
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: Deck,
            end: Deck,
            is_drowned: bool = False
    ) -> None:
        if start.row == end.row and start.column > end.column:
            start, end = end, start

        if start.column == end.column and start.row > end.row:
            start, end = end, start

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_full_ship_coords()

    def is_ship_vertical(self) -> bool:
        return self.start.column == self.end.column

    def is_ship_horizontal(self) -> bool:
        return self.start.row == self.end.row

    def ship_length(self) -> int:
        if self.is_ship_horizontal():
            return 1 + (self.end.column - self.start.column)
        if self.is_ship_vertical():
            return 1 + (self.end.row - self.start.row)
        raise ValueError(
            f"Ship must be either horizontal or "
            f"vertical! Got start={self.start}, end={self.end}"
        )

    def get_full_ship_coords(self) -> list[Deck]:
        ship_length = self.ship_length()

        is_vertical = self.is_ship_vertical()
        is_horizontal = self.is_ship_horizontal()

        if is_vertical or is_horizontal:
            ship_coords = [self.start]

            for index in range(1, ship_length):
                row_to_append = self.start.row
                column_to_append = self.start.column

                if is_vertical:
                    row_to_append += index
                elif is_horizontal:
                    column_to_append += index

                ship_coords.append(Deck(row_to_append, column_to_append))

            return ship_coords
        raise ValueError("Ship must be either horizontal or vertical!")

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError(f"No deck with coords: ({row}, {column})")

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if not deck.is_alive:
            return
        deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    FIELD_SIZE = 10

    def __init__(
            self,
            ships: list[tuple[tuple, tuple]]
    ) -> None:
        ships_objects = self._build_ships(ships)
        self._validate_field(ships_objects)
        self.field = self._build_field_dict(ships_objects)

    def _build_ships(
            self,
            ship_list: list[tuple[tuple, tuple]]
    ) -> list[Ship]:
        return [
            Ship(Deck(*start_coords), Deck(*end_coords))
            for start_coords, end_coords in ship_list
        ]

    def _build_field_dict(
            self,
            ship_list: list[Ship]
    ) -> dict:
        fields_dict = {}
        for ship in ship_list:
            for deck in ship.decks:
                fields_dict[(deck.row, deck.column)] = ship
        return fields_dict

    def _validate_field(self, ships: list[Ship]) -> None:
        self._validate_fleet_size(ships)
        self._validate_ships(ships)
        self._validate_fleet_composition(ships)
        self._validate_no_neighbors(ships)

    def _validate_fleet_size(self, ships: list[Ship]) -> None:
        if len(ships) != 10:
            raise ValueError(
                f"Invalid fleet size: expected 10 ships, got {len(ships)}."
            )

    def _validate_ships(self, ships: list[Ship]) -> None:
        for idx, ship in enumerate(ships, start=1):
            self._validate_orientation(ship, idx)
            self._validate_length(ship, idx)
            self._validate_in_bounds(ship, idx)

    def _validate_orientation(self, ship: Ship, idx: int) -> None:
        if not (ship.is_ship_horizontal() or ship.is_ship_vertical()):
            raise ValueError(
                f"Ship #{idx}: invalid orientation. "
                f"Ships must be placed strictly "
                f"horizontally or vertically. Got "
                f"start={ship.start}, end={ship.end}."
            )

    def _validate_length(self, ship: Ship, idx: int) -> None:
        length = ship.ship_length()
        if not (1 <= length <= 4):
            raise ValueError(
                f"Ship #{idx}: invalid length. "
                f"Ships must have length between 1 and 4. "
                f"Got length={length} for "
                f"start={ship.start}, end={ship.end}."
            )

    def _validate_in_bounds(self, ship: Ship, idx: int) -> None:
        for deck in ship.decks:
            if not (
                    0 <= deck.row < self.FIELD_SIZE
                    and 0 <= deck.column < self.FIELD_SIZE
            ):
                raise ValueError(
                    f"Ship #{idx}: coordinate out of "
                    f"bounds: ({deck.row}, {deck.column}). "
                    f"Allowed range is 0..{self.FIELD_SIZE - 1}. "
                    f"Ship start={ship.start}, end={ship.end}."
                )

    def _validate_fleet_composition(self, ships: list[Ship]) -> None:
        lengths = [ship.ship_length() for ship in ships]
        expected = {1: 4, 2: 3, 3: 2, 4: 1}
        names = {
            1: "single-deck",
            2: "double-deck",
            3: "three-deck",
            4: "four-deck"
        }

        for length, exp_count in expected.items():
            got = lengths.count(length)
            if got != exp_count:
                lengths_list = {
                    _length: lengths.count(_length)
                    for _length in sorted(set(lengths))
                }
                raise ValueError(
                    f"Invalid fleet composition: "
                    f"expected {exp_count} {names[length]} "
                    f"ship(s), got {got}. "
                    f"Actual counts by length: {lengths_list}."
                )

    def _validate_no_neighbors(self, ships: list[Ship]) -> None:
        forbidden = set()
        shifts = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]

        for ship in ships:
            decks = {(d.row, d.column) for d in ship.decks}

            conflicts = decks & forbidden
            if conflicts:
                raise ValueError(
                    f"Invalid ship placement: ships "
                    f"overlap or touch at {sorted(conflicts)}."
                )

            for row, column in decks:
                for dx, dy in shifts:
                    nr, nc = row + dx, column + dy
                    if 0 <= nr < self.FIELD_SIZE and 0 <= nc < self.FIELD_SIZE:
                        forbidden.add((nr, nc))

    def fire(self, location: tuple) -> str:
        try:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        except KeyError:
            return "Miss!"

    def print_field(self) -> None:
        grid = [
            ["~" for _ in range(self.FIELD_SIZE)]
            for _ in range(self.FIELD_SIZE)
        ]

        for (row, column), ship in self.field.items():
            cur_deck = ship.get_deck(row, column)

            if ship.is_drowned:
                grid[row][column] = "x"
            elif not cur_deck.is_alive:
                grid[row][column] = "*"
            else:
                grid[row][column] = u"\u25A1"

        for i, row_vals in enumerate(grid):
            if i == 0:
                print(
                    " ", " ".join(
                        str(num) for num in range(self.FIELD_SIZE)
                    )
                )
            print(i, " ".join(row_vals))
