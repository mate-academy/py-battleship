class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.start[0] == self.end[0]:
            for column_coordinate in range(self.start[1], self.end[1] + 1):
                deck = Deck(self.start[0], column_coordinate)
                self.decks.append(deck)
                self.is_horizontal = True
        elif self.start[1] == self.end[1]:
            for row_coordinate in range(self.start[0], self.end[0] + 1):
                deck = Deck(row_coordinate, self.start[1])
                self.decks.append(deck)
                self.is_horizontal = False
        else:
            raise ValueError(
                f"A Ship {(self.start, self.end)} cannot be diagonal."
            )

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    ADJACENT = object()

    def __init__(self, ships: list) -> None:
        self.field = {}

        for row_coordinate in range(0, 10):
            for column_coordinate in range(0, 10):
                self.field[(row_coordinate, column_coordinate)] = None

        ships_sorted = [tuple(sorted(ship)) for ship in ships]
        self.ships_obj = [Ship(ship[0], ship[1]) for ship in ships_sorted]
        self._validate_ships()

        for ship in self.ships_obj:
            adjacent_error = False

            for deck in ship.decks:
                if (deck.row, deck.column) not in self.field:
                    raise ValueError(
                        f"A Ship {(ship.start, ship.end)} "
                        f"is reaching out of battlefield."
                    )
                if isinstance(self.field[(deck.row, deck.column)], Ship):
                    raise ValueError(
                        f"A Ship {(ship.start, ship.end)} "
                        f"is on top of some other ship."
                    )
                if self.field[(deck.row, deck.column)] is self.ADJACENT:
                    adjacent_error = True
                self.field[(deck.row, deck.column)] = ship

            if adjacent_error:
                raise ValueError(
                    f"A Ship {(ship.start, ship.end)} "
                    f"is adjacent to some other ship."
                )
            to_make_adjacent = set()
            if ship.is_horizontal:
                for column_coordinate in range(
                    ship.start[1] - 1, ship.end[1] + 2
                ):
                    to_make_adjacent.add(
                        (ship.start[0] + 1, column_coordinate)
                    )
                    to_make_adjacent.add(
                        (ship.start[0] - 1, column_coordinate)
                    )
                to_make_adjacent.add((ship.start[0], ship.start[1] - 1))
                to_make_adjacent.add((ship.end[0], ship.end[1] + 1))
            else:
                for row_coordinate in range(
                    ship.start[0] - 1, ship.end[0] + 2
                ):
                    to_make_adjacent.add((row_coordinate, ship.start[1] + 1))
                    to_make_adjacent.add((row_coordinate, ship.start[1] - 1))
                to_make_adjacent.add((ship.start[0] - 1, ship.start[1]))
                to_make_adjacent.add((ship.end[0] + 1, ship.end[1]))

            for coordinates in to_make_adjacent:
                if (coordinates[0], coordinates[1]) in self.field:
                    self.field[(coordinates[0], coordinates[1])] = (
                        self.ADJACENT
                    )

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "You fired out of battlefield!"
        if not isinstance(self.field[location], Ship):
            return "Miss!"
        if self.field[location].is_drowned:
            return "Sunk!"
        if not self.field[location].get_deck(
            location[0], location[1]
        ).is_alive:
            return "Hit!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        str_battlefield = ""
        for key, value in self.field.items():
            if value is None or value is self.ADJACENT:
                str_battlefield += "  ~"
            elif value.is_drowned:
                str_battlefield += "  x"
            elif value.get_deck(key[0], key[1]).is_alive:
                str_battlefield += "  \u25a1"
            else:
                str_battlefield += "  *"
            if key[1] == 9:
                str_battlefield += "\n"
        print(str_battlefield)

    def _validate_ships(self) -> None:
        proper_ships = {1: 4, 2: 3, 3: 2, 4: 1}
        current_ships = {}
        for ship in self.ships_obj:
            if len(ship.decks) not in current_ships:
                current_ships[len(ship.decks)] = 1
            else:
                current_ships[len(ship.decks)] += 1
        try:
            assert dict(sorted(current_ships.items())) == proper_ships
        except AssertionError:
            raise ValueError("You have one or more ships of wrong decks size!")
