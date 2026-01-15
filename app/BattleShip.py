from app.Ship import Ship


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self._mark_forbidden_coordinates: set[tuple[int, int]] = set()
        self._field: dict[tuple[int, int], Ship] = {}
        self._field_ships(ships)
        try:
            self._validate_field(self._field)
        except ValueError as e:
            print(e)
            raise

    def _field_ships(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for ship_coordinates in ships:
            start = min(ship_coordinates)
            end = max(ship_coordinates)

            if not (start[0] == end[0] or start[1] == end[1]):
                print(
                    f"Invalid ship coordinates "
                    f"(not straight): {start} -> {end}"
                )
                continue

            ship = Ship(start, end)

            if any(
                    (deck.row, deck.column) in self._mark_forbidden_coordinates
                    for deck in ship.decks
            ):
                print(
                    f"The coordinates {start} → {end} are "
                    f"occupied or too close to another ship."
                )
                continue

            self._field.update(
                {(deck.row, deck.column): ship for deck in ship.decks}
            )
            self._forbidden_coordinates_(start, end, ship)

    def fire(self, location: tuple[int, int]) -> str:
        if not (0 <= location[0] <= 9 and 0 <= location[1] <= 9):
            return f"The location {location} does not exist."
        elif location not in self._field:
            return "Miss!"
        else:
            ship = self._field[location]
            hit = ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            last_deck = sum(
                1 for deck in ship.decks if deck.is_alive is True
            ) == 1
            if last_deck:
                print("The last deck left.")
            if hit:
                return "Hit!"

    def _forbidden_coordinates_(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            ship: Ship
    ) -> None:
        row = max(start[0] - 1, 0)
        col = max(start[1] - 1, 0)

        length = len(ship.decks)
        weight = 2

        is_horizontal = ship.is_horizontal or len(ship.decks) == 1

        if is_horizontal:
            if start[1] > 0 and end[1] < 9:
                length += 1
            if start[0] > 0 and end[0] < 9:
                weight += 1
        else:
            if start[1] > 0 and end[1] < 9:
                weight += 1
            if start[0] > 0 and end[0] < 9:
                length += 1

        for _ in range(length + 1):
            if 0 <= col <= 9 and 0 <= row <= 9:
                if is_horizontal:
                    row_ = row
                    for _ in range(weight):
                        self._mark_forbidden_coordinates.add((row_, col))
                        row_ += 1
                    col += 1
                else:
                    col_ = col
                    for _ in range(weight):
                        self._mark_forbidden_coordinates.add((row, col_))
                        col_ += 1
                    row += 1
            else:
                break

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) not in self._field:
                    print("~", end="      ")
                else:
                    ship = self._field[(row, col)]
                    if ship.is_drowned:
                        print("X", end="      ")
                        continue

                    is_alive = next(
                        deck.is_alive
                        for deck in ship.decks
                        if (deck.row, deck.column) == (row, col)
                    )
                    if is_alive:
                        print(u"\u25A1", end="      ")
                    else:
                        print("*", end="      ")
            print()
        print()

    def _validate_field(self, field: dict[tuple[int, int], Ship]) -> None:
        single_deck_ships = []
        double_deck_ships = []
        three_deck_ships = []
        four_deck_ships = []

        for ship in set(field.values()):
            length_ship = len(ship.decks)
            ship_coordinate = (
                (ship.decks[0].row, ship.decks[0].column),
                (ship.decks[len(ship.decks) - 1].row,
                 ship.decks[len(ship.decks) - 1].column)
            )
            if length_ship == 1 and len(single_deck_ships) < 4:
                single_deck_ships.append(ship)
            elif length_ship == 2 and len(double_deck_ships) < 3:
                double_deck_ships.append(ship)
            elif length_ship == 3 and len(three_deck_ships) < 2:
                three_deck_ships.append(ship)
            elif length_ship == 4 and len(four_deck_ships) != 1:
                four_deck_ships.append(ship)
            else:
                raise ValueError(
                    f"There are already enough ships "
                    f"with length {length_ship}."
                    f"Coordinate: {ship_coordinate}"
                )
