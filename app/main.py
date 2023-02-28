class ShipPlacementError(Exception):
    def __str__(self) -> str:
        return "Invalid ship placement on the field!"


class FieldValidationError(Exception):
    def __str__(self) -> str:
        return "Ships are placed not according to the rules!"


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return str(self.row) + str(self.column)


class Ship:
    def __init__(
        self,
        start: tuple[int],
        end: tuple[int],
        is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        self.deck_count = 0
        self._build_ship(start, end)

    def __repr__(self) -> str:
        return "".join(str(deck) for deck in self.decks)

    def _build_ship(self, start: tuple[int], end: tuple[int]) -> None:
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
                self.deck_count += 1

    def get_deck(self, row: int, column: int) -> str:
        if self.is_drowned:
            return "x"
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return "\u25A1" if deck.is_alive else "*"

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                self.deck_count -= 1
                if self.deck_count == 0:
                    self.is_drowned = True
                    return "Sunk!"
                return "Hit!"


class Battleship:
    SIZE = 10

    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self._set_ships(ships)

    def _set_ships(self, ships: list[tuple]) -> None:
        for ship_start, ship_end in ships:
            if not (
                self._validate_cell(ship_start)
                and self._validate_cell(ship_end)
                and (ship_start[0] == ship_end[0]
                     or ship_start[1] == ship_end[1])
            ):
                raise ShipPlacementError
            new_ship = Ship(ship_start, ship_end)
            for deck in new_ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ShipPlacementError
                self.field[(deck.row, deck.column)] = new_ship
        if not self._validate_field():
            raise FieldValidationError

    def _validate_field(self) -> bool:
        ship_rules = {4: 1, 3: 2, 2: 3, 1: 4}
        fleet = {}
        for cell, shipdeck in self.field.items():
            if not self._proximity_check(cell):
                return False
            if shipdeck.deck_count not in fleet:
                fleet[shipdeck.deck_count] = set()
            fleet[shipdeck.deck_count].add(str(shipdeck))
        if len(fleet) != len(ship_rules):
            return False
        for ship, count in ship_rules.items():
            if ship not in fleet or len(fleet[ship]) != count:
                return False
        return True

    def _proximity_check(self, check_cell: tuple[int]) -> bool:
        dirs = [
            (-1, -1), (-1, 0), (-1, +1),
            (0, +1), (0, -1),
            (+1, -1), (+1, 0), (+1, +1)
        ]
        for dir_y, dir_x in dirs:
            nei_cell = (check_cell[0] + dir_y, check_cell[1] + dir_x)
            if self._validate_cell(nei_cell):
                if (
                    nei_cell in self.field
                    and self.field[nei_cell] is not self.field[check_cell]
                ):
                    return False
        return True

    def _validate_cell(self, cell: tuple[int]) -> bool:
        return (
            0 <= cell[0] < Battleship.SIZE
            and 0 <= cell[1] < Battleship.SIZE
        )

    def fire(self, location: tuple[int]) -> str:
        if not self._validate_cell(location):
            return "Critical miss! (invalid location input)"
        if location in self.field and not self.field[location].is_drowned:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        for row in range(Battleship.SIZE):
            for col in range(Battleship.SIZE):
                if (row, col) in self.field:
                    print(self.field[(row, col)].get_deck(row, col), end="\t")
                else:
                    print("~", end="\t")
            print()
