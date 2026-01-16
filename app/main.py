class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (f"Deck(row={self.row}, "
                f"column={self.column}, "
                f"is_alive={self.is_alive})")


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        self.decks = self._create_deck_list(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def _create_deck_list(start: tuple[int, int],
                          end: tuple[int, int]
                          ) -> list[Deck]:
        result = []
        row_dist = abs(start[0] - end[0])
        col_dist = abs(start[1] - end[1])
        for row in range(row_dist + 1):
            for column in range(col_dist + 1):
                result.append(Deck(start[0] + row, start[1] + column))
        return result

    def get_deck(self, row: int, column: int) -> Deck:
        return next(deck for deck in self.decks
                    if deck.row == row and deck.column == column)

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])

    def __repr__(self) -> str:
        return f"Ship(decks={self.decks}, is_drowned={self.is_drowned})"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.fields = {}
        for ship in ships:
            if isinstance(ship, tuple):
                new_ship = Ship(*ship)
                for deck in new_ship.decks:
                    self.fields[(deck.row, deck.column)] = new_ship
            else:
                raise ValueError(f"{ship} is not instance of tuple")
        try:
            self._validate_field()
        except ValueError as e:
            print(e)

    def _validate_field(self) -> None:
        ships = set()
        for row in range(10):
            for column in range(10):
                ship = self.fields.get((row, column), None)
                if ship:
                    ships.add(ship)

        self._validate_ship_count(ships)
        self._validate_ship_collision(ships)

    @staticmethod
    def _validate_ship_count(ships: set[Ship]) -> None:
        ship_count = [0] * 4
        for ship in ships:
            ship_count[len(ship.decks) - 1] += 1

        if ship_count[0] != 4:
            raise ValueError(f"Expected 4 single-deck ships, "
                             f"got {ship_count[0]}")
        if ship_count[1] != 3:
            raise ValueError(f"Expected 3 double-deck ships, "
                             f"got {ship_count[1]}")
        if ship_count[2] != 2:
            raise ValueError(f"Expected 2 three-deck ships, "
                             f"got {ship_count[2]}")
        if ship_count[3] != 1:
            raise ValueError(f"Expected 1 four-deck ships, "
                             f"got {ship_count[3]}")
        if sum(ship_count) != 10:
            raise ValueError(f"Expected 10 ships, "
                             f"got {sum(ship_count)}")

    def _validate_ship_collision(self, ships: set[Ship]) -> None:
        for ship in ships:
            for deck in ship.decks:
                for row in range(-1, 2):
                    for column in range(-1, 2):
                        location = (
                            min(max(0, deck.row + row), 9),
                            min(max(0, deck.column + column), 9)
                        )
                        field = self.fields.get(location, None)
                        if field is not None and field is not ship:
                            raise ValueError(f"Ship: {ship} "
                                             f"collide with {field}")

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.fields.get(location, None)
        if ship:
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.fields.get((row, column), None)
                if ship:
                    if ship.is_drowned:
                        print("x ", end="")
                    elif not ship.get_deck(row, column).is_alive:
                        print("* ", end="")
                    else:
                        print(u"\u25A1 ", end="")
                else:
                    print("~ ", end="")
            print("")
