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


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:

        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0] and start[1] == end[1]:
            self.decks.append(Deck(start[0], start[1]))
        elif start[0] == end[0]:
            for y_coord in range(min(start[1], end[1]),
                                 max(start[1], end[1]) + 1):
                self.decks.append(Deck(start[0], y_coord))
        elif start[1] == end[1]:
            for x_coord in range(min(start[0], end[0]),
                                 max(start[0], end[0]) + 1):
                self.decks.append(Deck(x_coord, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self._validate_ships_placement()

    def fire(self, location: tuple[int, int]) -> str:
        for key, ship in self.field.items():
            start, end = key
            if (
                start[0] <= location[0] <= end[0]
                and start[1] <= location[1] <= end[1]
                and not ship.is_drowned
            ):
                result = ship.fire(location[0], location[1])
                self.print_field()
                return result
        self.print_field()
        return "Miss!"

    def print_field(self) -> None:
        for line in range(10):
            line_field = ["~" for _ in range(10)]
            for key, ship in self.field.items():
                if key[0][0] <= line <= key[1][0] and not ship.is_drowned:
                    for deck in ship.decks:
                        if deck.row == line:
                            if not deck.is_alive:
                                line_field[deck.column] = "*"
                            else:
                                line_field[deck.column] = "\u25A1"
            print("  ".join(line_field))

    def _validate_ships_placement(self) -> None:
        temp_field = {}
        for ship in self.ships:
            start, end = ship
            if not (
                0 <= start[0] <= 9
                and 0 <= start[1] <= 9
                and 0 <= end[0] <= 9
                and 0 <= end[1] <= 9
            ):
                raise ValueError(
                    "Ships must be within the bounds of the 10x10 grid."
                )
            if start[0] != end[0] and start[1] != end[1]:
                raise ValueError(
                    "Ships must be either horizontal or vertical."
                )
            for x_coord in range(start[0], end[0] + 1):
                for y_coord in range(start[1], end[1] + 1):
                    if (x_coord, y_coord) in temp_field:
                        raise ValueError(
                            "Ships cannot intersect or touch each other."
                        )
                    temp_field[(x_coord, y_coord)] = True
        self.field = {ship: Ship(ship[0], ship[1]) for ship in self.ships}
