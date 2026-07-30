class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.deck = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        if start == end:
            self.decks = [Deck(*start)]
        else:
            if start[0] == end[0]:
                self.decks = [
                    Deck(start[0], y) for y in range(start[1], end[1] + 1)
                ]
            if start[1] == end[1]:
                self.decks = [
                    Deck(x, start[1]) for x in range(start[0], end[0] + 1)
                ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.deck == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        self._validate_ships()

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field.keys():
                    if self.field[(row, column)].is_drowned:
                        print(" x", end=" ")
                    else:
                        if (
                            self.field[(row, column)]
                            .get_deck(row, column)
                            .is_alive
                        ):  # noqa E501
                            print(" \u25a1", end=" ")
                        else:
                            print(" *", end=" ")
                else:
                    print(" ~", end=" ")
            print()

    def _validate_distance(self, ship: tuple) -> None:
        if self.field:
            for point in ship:
                for row in range(point[0] - 1, point[0] + 2):
                    for column in range(point[1] - 1, point[1] + 2):
                        if (row, column) in self.field.keys():
                            raise Exception(
                                "There must be a distance between ships, "
                                "at least one cell."
                            )

    def _validate_ships(self) -> None:
        ships_count = {4: 1, 3: 2, 2: 3, 1: 4}
        if len(self.ships) != 10:
            raise Exception("There should be 10 ships on the field.")
        for ship_coord in self.ships:
            self._validate_distance(ship_coord)
            ship = Ship(*ship_coord)
            decks_count = len(ship.decks)
            if decks_count in ships_count.keys():
                if ships_count[decks_count] == 0:
                    raise Exception(
                        f"All {decks_count}-deck ships "
                        f"have already been created."
                    )
                ships_count[decks_count] -= 1
            self.field.update({deck.deck: ship for deck in ship.decks})
