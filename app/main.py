class BattleshipActivationError(Exception):
    def __init__(
            self,
            message: str = "Creating ships doesn't meet the conditions!"
    ) -> None:
        super().__init__(message)


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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.forbidden_cells = set()
        self.decks = self.set_decks_list(self.start, self.end)

    def set_decks_list(
            self,
            start_point: tuple,
            end_point: tuple
    ) -> list[Deck]:
        row_s, column_s = start_point
        row_e, column_e = end_point
        self.get_forbidden_cells(row_s, column_s, row_e, column_e)
        if row_s == row_e:
            return [
                Deck(row_s, point) for point
                in range(column_s, column_e + 1)
            ]
        return [
            Deck(point, column_s) for point
            in range(row_s, row_e + 1)
        ]

    def get_forbidden_cells(
            self,
            row_start: int,
            column_start: int,
            row_end: int,
            column_end: int
    ) -> None:
        for row in range(max(0, row_start - 1), min((row_end + 2), 10)):
            for column in range(
                    max(0, column_start - 1),
                    min((column_end + 2), 10)
            ):
                self.forbidden_cells.add((row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for el in self.decks:
            if el.row == row and el.column == column:
                return el

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = self.get_field()
        self._validate_field(self.ships)

    def get_field(self) -> dict:
        field = {}
        for ship in self.ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    @staticmethod
    def _validate_field(ships: list[Ship]) -> None:
        if len(ships) != 10:
            raise BattleshipActivationError(
                "The total number of the ships should be 10!"
            )

        deck_counter = {
            1: [0, 4, "single-deck"],
            2: [0, 3, "double-deck"],
            3: [0, 2, "three-deck"],
            4: [0, 1, "four-deck"]
        }
        for ship in ships:
            deck_counter[len(ship.decks)][0] += 1
        for key, value in deck_counter.items():
            if value[0] != value[1]:
                raise BattleshipActivationError(
                    f"There should be {value[1]} {value[2]} "
                    f"ships, you have {value[0]}!"
                )

        forbidden_area = set()
        for ship in ships:
            for el in ((deck.row, deck.column) for deck in ship.decks):
                if el in forbidden_area:
                    raise BattleshipActivationError(
                        f"It is impossible to place the ship here {el}!"
                    )
            forbidden_area.update(ship.forbidden_cells)

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        base_field = [["~" for _ in range(10)] for _ in range(10)]

        for location, ship in self.field.items():
            row, column = location
            if ship.is_drowned:
                base_field[row][column] = "X"
            elif ship.get_deck(row, column).is_alive:
                base_field[row][column] = "\u25A1"
            else:
                base_field[row][column] = "\u26A1"

        for line in base_field:
            print(line)
        print("___________________________________________________")
        print("'\u25A1' - alive, '\u26A1' - hit, 'X' - drowned\n")
