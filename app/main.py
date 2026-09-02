class IncorrectShipPosition(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int , is_alive: bool = True) -> None:
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
        self.decks = [Deck(deck[0], deck[1], True)
                      for deck in get_coordinates((start, end))]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self._validate_field(ships)
        self.field = {
            cell: ship_obj
            for ship in ships
            for ship_obj in [Ship(ship[0], ship[1], False)]
            for cell in get_coordinates(ship)
        }

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]

        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        field[row][column] = "x"
                    else:
                        if ship.get_deck(row, column).is_alive:
                            field[row][column] = "□"
                        else:
                            field[row][column] = "*"

        for row in range(10):
            print(" ".join(field[row]))

    def _validate_field(self, ships: list) -> None:
        ship_count_on_decks = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in ships:
            try:
                ship_count_on_decks[abs(sum(ship[1]) - sum(ship[0])) + 1] += 1
            except KeyError:
                raise IncorrectShipPosition

        if ship_count_on_decks != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise IncorrectShipPosition

        list_fill_cells = []
        for ship in ships:
            cells = get_coordinates(ship)

            if any(cell in list_fill_cells for cell in cells):
                raise IncorrectShipPosition

            for cell in cells:
                for dx in (cell[0] - 1, cell[0], cell[0] + 1):
                    for dy in (cell[1] - 1, cell[1], cell[1] + 1):
                        list_fill_cells.append((dx, dy))


def get_coordinates(ship: list) -> list:
    size = abs(sum(ship[1]) - sum(ship[0])) + 1

    iterable_order = "y"

    if ship[0][0] != ship[1][0]:
        iterable_order = "x"

    start_coordinates = list(ship[0])
    coordinates = [tuple(start_coordinates)]

    for i in range(size - 1):
        if iterable_order == "x":
            start_coordinates[0] += 1
        else:
            start_coordinates[1] += 1
        coordinates.append(tuple(start_coordinates))

    return coordinates
