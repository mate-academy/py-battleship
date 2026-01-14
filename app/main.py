class ValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row, self.column, self.is_alive = row, column, is_alive

    def __repr__(self) -> str:
        return f"Deck({self.column}, {self.row})"

    def __eq__(self, other: tuple[int, int]) -> bool:
        return self.row == other[1] and self.column == other[0]


class Ship:
    def __init__(
        self,
        coords: tuple[tuple[int, int], tuple[int, int]],
        is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        start = {
            "row": coords[0][1],
            "column": coords[0][0],
        }
        end = {
            "row": coords[1][1],
            "column": coords[1][0],
        }

        if start["row"] == end["row"]:
            # Horizontal ship
            row = start["row"]
            col_start = min(start["column"], end["column"])
            col_end = max(start["column"], end["column"])
            self.decks = [
                Deck(row=row, column=col)
                for col in range(col_start, col_end + 1)
            ]

        elif start["column"] == end["column"]:
            # Vertical ship
            column = start["column"]
            row_start = min(start["row"], end["row"])
            row_end = max(start["row"], end["row"])
            self.decks = [
                Deck(row=row, column=column)
                for row in range(row_start, row_end + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck | bool:
        try:
            return self.decks[self.decks.index((column, row))]
        except ValueError:
            return False

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self, ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = [Ship(ship_data) for ship_data in ships]
        self.field = []
        self.re_draw_field()

        if not self._validate_field():
            raise ValidationError("Errors in field validation:")

    def is_ship_in_coord(self, coord: tuple[int, int]) -> tuple | bool:
        for ship in self.ships:
            deck = ship.get_deck(row=coord[1], column=coord[0])
            if deck:
                return deck, ship
        return False

    def _validate_field(self) -> bool:
        is_ok = True
        ships_lengths = [len(ship.decks) for ship in self.ships]
        checks = [
            (
                len(self.ships) == 10,
                "Must be 10 ships!"
            ),
            (
                ships_lengths.count(1) == 4,
                "There should be 4 single-deck ships!"
            ),
            (
                ships_lengths.count(2) == 3,
                "There should be 3 double-deck ships!"
            ),
            (
                ships_lengths.count(3) == 2,
                "There should be 2 three-deck ships!"
            ),
            (
                ships_lengths.count(4) == 1,
                "There should be 1 four-deck ship!"
            ),
            (
                all(not self.are_ships_nearby(ship) for ship in self.ships),
                "Ships shouldn't be located in the neighboring cells!",
            ),
        ]

        for condition, info in checks:
            if not condition:
                red = "\033[31m"
                print(f"{red}{info}")

                is_ok = False

        return is_ok

    def are_ships_nearby(self, ship: Ship) -> bool:
        for deck in ship.decks:
            for row in range(deck.row - 1, deck.row + 2):
                for column in range(deck.column - 1, deck.column + 2):
                    if (row, column) != (deck.row, deck.column):
                        for other_ship in self.ships:
                            if other_ship == ship:
                                continue
                            for other_deck in other_ship.decks:
                                if (row, column) == (
                                    other_deck.row, other_deck.column
                                ):
                                    return True
        return False

    def re_draw_field(self) -> None:
        def get_symbol_of_deck(field_data: tuple[Deck, Ship] | bool) -> str:
            if not field_data:
                return "~"

            deck, ship = field_data

            if deck.is_alive:
                return "□"
            if ship.is_drowned:
                return "x"
            return "*"

        self.field = [
            [
                get_symbol_of_deck(self.is_ship_in_coord((column, row)))
                for row in range(10)
            ]
            for column in range(10)
        ]

    def fire(self, location: tuple[int, int]) -> str:
        location_row = location[1]
        location_column = location[0]
        current_ship = None
        curr_deck = None

        for ship in self.ships:
            curr_deck = ship.get_deck(row=location_row, column=location_column)
            if curr_deck:
                current_ship = ship
                break
        message = ""
        if not current_ship:
            message = "Miss!"

        elif current_ship and curr_deck and curr_deck.is_alive:
            current_ship.fire(row=location_row, column=location_column)

            if current_ship.is_drowned:
                message = "Sunk!"
            else:
                message = "Hit!"

        print(message)
        return message

    def print_field(self) -> None:
        self.re_draw_field()
        for column in self.field:
            print("   ".join(column))
