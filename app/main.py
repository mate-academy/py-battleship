FIELD_SIZE = 10
SHIPS_TOTAL_NUMBER = 10
SINGLE_DECK_SHIPS_NUMBER = 4
DOUBLE_DECK_SHIPS_NUMBER = 3
THREE_DECK_SHIPS_NUMBER = 2
FOUR_DECK_SHIPS_NUMBER = 1


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        is_horizontal = Ship.define_is_horizontal(start[0], end[0])
        self.decks = []

        if is_horizontal:
            self.decks = [Deck(start[0], i, not is_drowned)
                          for i in range(start[1], end[1] + 1)]
        else:
            self.decks = [Deck(i, start[1], not is_drowned)
                          for i in range(start[0], end[0] + 1)]

        self.is_drowned = is_drowned

    @staticmethod
    def define_is_horizontal(start_row: int, end_row: int) -> bool:
        return start_row == end_row

    def check_is_ship_afloat(self) -> bool:
        return any(deck.is_alive for deck in self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        found_decks = list(filter(lambda deck: deck.row == row and deck
                                  .column == column, self.decks))

        return found_decks[0]

    def fire(self, row: int, column: int) -> bool:
        target_deck = self.get_deck(row, column)

        target_deck.is_alive = False

        if not self.check_is_ship_afloat():
            self.is_drowned = True

        return self.is_drowned


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            self.create_cells_from_the_ship(new_ship)

        self._validate_field()

    def get_all_ships(self) -> list[Ship]:
        field_ships = []

        for cell in self.field.values():
            if cell not in field_ships:
                field_ships.append(cell)

        return field_ships

    @staticmethod
    def get_ships_number_with_n_decks(ships: list[Ship],
                                      decks_number: int) -> int:
        return len([ship for ship in ships
                    if len(ship.decks) == decks_number])

    @staticmethod
    def are_coords_inside_field(row: int, col: int) -> bool:
        return (-1 < row < FIELD_SIZE) and (-1 < col < FIELD_SIZE)

    def is_another_ship(self, coords: tuple, ship: Ship) -> bool:
        if Battleship.are_coords_inside_field(coords[0], coords[1]):
            return coords in self.field and self.field[coords] != ship

        return False

    def check_is_deck_touches_another_ship(self, coords: tuple,
                                           ship: Ship) -> None:
        for row in range(-1, 2):
            for col in range(-1, 2):
                row_for_check = coords[0] + row
                col_for_check = coords[1] + col

                if self.is_another_ship((row_for_check, col_for_check),
                                        ship):
                    raise ValueError("The ships shouldn't touch each other")

    def _validate_field(self) -> None:
        field_ships = self.get_all_ships()

        if len(field_ships) != SHIPS_TOTAL_NUMBER:
            raise ValueError(f"""You should provide the battlefield
                with {SHIPS_TOTAL_NUMBER} ships""")

        if self.get_ships_number_with_n_decks(
                field_ships, 1) != SINGLE_DECK_SHIPS_NUMBER:
            raise ValueError(f"""You should provide the battlefield
                with {SINGLE_DECK_SHIPS_NUMBER} single-deck ships""")

        if self.get_ships_number_with_n_decks(
                field_ships, 2) != DOUBLE_DECK_SHIPS_NUMBER:
            raise ValueError(f"""You should provide the battlefield
                with {DOUBLE_DECK_SHIPS_NUMBER} double-deck ships""")

        if self.get_ships_number_with_n_decks(
                field_ships, 3) != THREE_DECK_SHIPS_NUMBER:
            raise ValueError(f"""You should provide the battlefield
                with {THREE_DECK_SHIPS_NUMBER} three-deck ships""")

        if self.get_ships_number_with_n_decks(
                field_ships, 4) != FOUR_DECK_SHIPS_NUMBER:
            raise ValueError(f"""You should provide the battlefield
                with {FOUR_DECK_SHIPS_NUMBER} four-deck ships""")

        for coords in self.field:
            self.check_is_deck_touches_another_ship(coords, self.field[coords])

    def create_cells_from_the_ship(self, ship: Ship) -> None:
        for deck in ship.decks:
            self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        try:
            fire_result = self.field[location].fire(location[0], location[1])

            return "Sunk!" if fire_result else "Hit!"
        except KeyError:
            return "Miss!"

    def get_ship_deck_picture(self, row: int, col: int) -> str:
        ship = self.field[(row, col)]
        deck = ship.get_deck(row, col)

        if ship.is_drowned:
            return "x"
        elif deck.is_alive:
            return u"\u25A1"
        else:
            return "*"

    def print_field_cell(self, row: int, col: int) -> None:
        symbol_to_print = "~"
        end_symbol = "\n" if col == FIELD_SIZE - 1 else "   "

        if (row, col) in self.field:
            symbol_to_print = self.get_ship_deck_picture(row, col)

        print(symbol_to_print, end=end_symbol)

    def print_field(self) -> None:
        for row in range(FIELD_SIZE):
            for col in range(FIELD_SIZE):
                self.print_field_cell(row, col)
