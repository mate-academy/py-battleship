class ValidateInputError(Exception):
    """"Exception for incorrect input coordinates"""

    def __str__(self):
        return "Incorrect coordinates. (only in range 0-9)"


class ValidateFieldError(Exception):
    """"Exception for incorrect field"""


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self._create_decks()

    def _create_decks(self):
        if (self.start[1] or self.start[0]) > 9 or \
                (self.start[1] or self.start[0]) < 0:
            raise ValidateInputError
        if (self.end[1] or self.end[0]) > 9 or \
                (self.end[1] or self.end[0]) < 0:
            raise ValidateInputError

        if self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

        elif self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        if 0 <= row <= 9 and 0 <= column <= 9:
            deck_disable = self.get_deck(row, column)
            deck_disable.is_alive = False
            if not any([deck.is_alive for deck in self.decks]):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list):
        self.ships = ships
        self.field = {}
        self._fill_field()
        self._validate_field()

    def _fill_field(self):
        for ship in self.ships:
            start, end = ship
            fill_ship = Ship(start, end)
            if start[1] == end[1]:
                for row in range(start[0], end[0] + 1):
                    self.field[(row, start[1])] = fill_ship

            elif start[0] == end[0]:
                for column in range(start[1], end[1] + 1):
                    self.field[(start[0], column)] = fill_ship

    def fire(self, location: tuple):
        row, column = location
        if location in self.field:
            ship_disable = self.field[location]
            ship_disable.fire(row, column)
            if ship_disable.is_drowned:
                return "Sunk!"
            return "Hit!"
        self.field[(row, column)] = "Miss!"
        return "Miss!"

    def print_field(self):

        list_decks = []

        for line in self.field:
            list_decks.append(line)

        list_decks.sort()

        for index_line in range(10):
            line_field = ["~" for _ in range(10)]
            for line in list_decks:
                if line[0] == index_line:
                    if self.field[line] == "Miss!":
                        line_field[line[1]] = "m"
                    elif self.field[line].is_drowned:
                        line_field[line[1]] = "x"
                    elif not self.field[line].get_deck(
                            line[0], line[1]).is_alive:
                        line_field[line[1]] = "*"
                    elif not self.field[line].is_drowned:
                        line_field[line[1]] = "\u25A1"

            print('  '.join(line_field))

    def _validate_field(self):
        if len(self.ships) == 10:
            all_ships = {1: 0, 2: 0, 3: 0, 4: 0}
            size_ship = 0

            for ship in self.ships:
                start, end = ship

                if start[1] == end[1]:
                    size_ship = end[0] - start[0]

                    check_coord = (
                        (start[1], start[0] - 1), (start[1], end[0] + 1)
                    )
                    for check_column, check_row in check_coord:
                        if (check_row, check_column) in self.field:
                            raise ValidateFieldError(
                                "ships shouldn't be located in the"
                                " neighboring cells (even if cells"
                                " are neighbors by diagonal)")

                    for check_column in (start[1] - 1, start[1] + 1):
                        for check_row in range(start[0] - 1, end[0] + 2):
                            check_position = (check_row, check_column)

                            if check_position in self.field:
                                raise ValidateFieldError(
                                    "ships shouldn't be located in the"
                                    " neighboring cells (even if cells"
                                    " are neighbors by diagonal)")

                elif start[0] == end[0]:
                    size_ship = end[1] - start[1]

                    check_coord = (
                        (start[0], start[1] - 1), (start[0], end[1] + 1)
                    )
                    for check_row, check_column in check_coord:
                        if (check_row, check_column) in self.field:
                            raise ValidateFieldError(
                                "ships shouldn't be located in the"
                                " neighboring cells (even if cells"
                                " are neighbors by diagonal)")

                    for check_row in (start[0] - 1, start[0] + 1):
                        for check_column in range(start[1] - 1, end[1] + 2):
                            check_position = (check_row, check_column)
                            if check_position in self.field:
                                raise ValidateFieldError(
                                    "ships shouldn't be located in the"
                                    " neighboring cells (even if cells"
                                    " are neighbors by diagonal)")

                all_ships[size_ship + 1] += 1

            self._check_all_ships(all_ships)

        else:
            raise ValidateFieldError("The total number"
                                     " of the ships should be 10")

    @staticmethod
    def _check_all_ships(ships):
        if ships[1] != 4:
            raise ValidateFieldError("there should be 4 single-deck ships")
        if ships[2] != 3:
            raise ValidateFieldError("there should be 3 double-deck ships")
        if ships[3] != 2:
            raise ValidateFieldError("there should be 2 three-deck ships")
        if ships[4] != 1:
            raise ValidateFieldError("there should be 1 four-deck ship")


if __name__ == "__main__":
    """"
    Extra:
    Tests for print field
    """
battle_ship = Battleship(
    ships=[
        ((2, 0), (2, 3)),
        ((4, 5), (4, 6)),
        ((3, 8), (3, 9)),
        ((6, 0), (8, 0)),
        ((6, 4), (6, 6)),
        ((6, 8), (6, 9)),
        ((9, 9), (9, 9)),
        ((9, 5), (9, 5)),
        ((9, 3), (9, 3)),
        ((9, 7), (9, 7)),
    ]
)

print(battle_ship.fire((2, 0)))
battle_ship.print_field()
print(battle_ship.fire((2, 1)))
battle_ship.print_field()
print(battle_ship.fire((2, 2)))
battle_ship.print_field()
print(battle_ship.fire((2, 3)))
battle_ship.print_field()
print(battle_ship.fire((2, 4)))
battle_ship.print_field()
print(battle_ship.fire((2, 5)))
print(battle_ship.fire((4, 9)))
battle_ship.print_field()
