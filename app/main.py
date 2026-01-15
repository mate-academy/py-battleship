class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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

        if Ship.check_is_ship_horizontal_or_single_deck(start, end):
            self.horizontal = True
            self.decks = [Deck(start[0], column)
                          for column in range(start[1], end[1] + 1)]
        else:
            self.horizontal = False
            self.decks = [Deck(row, start[1])
                          for row in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        if self.horizontal:
            return self.decks[column - self.decks[0].column]
        return self.decks[row - self.decks[0].row]

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not self.check_is_ship_alive():
            self.is_drowned = True

    def check_is_ship_alive(self) -> bool:
        return any(deck.is_alive for deck in self.decks)

    @staticmethod
    def check_is_ship_horizontal_or_single_deck(
            start: tuple,
            end: tuple
    ) -> bool:
        return start[0] == end[0]


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        ships_instances_list = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {(deck.row, deck.column): ship
                      for ship in ships_instances_list
                      for deck in ship.decks}
        if not self._validate_field(ships_instances_list):
            raise Exception("Such a field cannot be created")

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            output = ""
            for column in range(0, 10):
                potential_ship = self.field.get((row, column))
                if potential_ship:
                    if potential_ship.is_drowned:
                        output += "x "
                    elif potential_ship.get_deck(row, column).is_alive:
                        output += "□ "
                    else:
                        output += "* "
                else:
                    output += "~ "
            print(output)

    def _validate_field(self, ships: list[Ship]) -> bool:
        if len(ships) != 10:
            return False
        ship_length = [len(ship.decks) for ship in ships]
        ship_count_by_length = {length: ship_length.count(length)
                                for length in set(ship_length)}
        required = {
            1: 4,
            2: 3,
            3: 2,
            4: 1
        }
        if ship_count_by_length != required:
            return False
        for ship in ships:
            if not self._check_if_space_empty_around_ship(ship):
                return False
        return True

    def _check_if_space_empty_around_ship(self, ship: Ship) -> bool:
        if ship.horizontal:
            for row in range(
                    max(0, ship.decks[0].row - 1),
                    min(9, ship.decks[0].row + 1)
            ):
                for column in range(
                        max(0, ship.decks[0].column - 1),
                        min(9, ship.decks[-1].column + 1)
                ):
                    if not self._check_is_field_empty_or_given_ship(
                            ship,
                            (row, column)
                    ):
                        return False
            return True
        for row in range(
                max(0, ship.decks[0].row - 1),
                min(9, ship.decks[-1].row + 1)
        ):
            for column in range(
                    max(0, ship.decks[0].column - 1),
                    min(9, ship.decks[0].column + 1)
            ):
                if not self._check_is_field_empty_or_given_ship(
                        ship,
                        (row, column)
                ):
                    return False
        return True

    def _check_is_field_empty_or_given_ship(
            self,
            ship: Ship,
            location: tuple[int, int]
    ) -> bool:

        if self.field.get((location[0], location[1])):
            if self.field[(location[0], location[1])] != ship:
                return False
        return True
