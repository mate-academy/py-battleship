class IncorrectDataInput(Exception):
    pass


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

    def __repr__(self) -> str:
        return f"deck: locating{self.row, self.column}"


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.start_row, self.start_column = start
        self.end_row, self.end_column = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column) for row, column in self.complete_ship()
        ]

    def __repr__(self) -> str:
        return f"Ship{self.start, self.end}"

    def complete_ship(self) -> list[tuple]:
        if self.start_row == self.end_row:
            return [
                (self.start_row, column)
                for column in range(self.start_column, self.end_column + 1)
            ]
        else:
            return [
                (row, self.start_column)
                for row in range(self.start_row, self.end_row + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ship_instances = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ship_instances:
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    self.print_field()
                    raise IncorrectDataInput(
                        f"{ship} can not be located as the cell"
                        f" {deck.row, deck.column} is allready ocupied"
                    )
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        damaged_ship = self.field.get(location)
        if damaged_ship and not damaged_ship.is_drowned:
            damaged_ship.fire(*location)
            return "Hit!" if not damaged_ship.is_drowned else "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        field = {row: ["~" for _ in range(10)] for row in range(10)}
        for location, ship in self.field.items():
            row, column = location
            if ship.is_drowned:
                field[row][column] = "x"
            elif ship.get_deck(*location).is_alive:
                field[row][column] = "\u25A1"
            else:
                field[row][column] = "*"

        print("\n", end="")
        print("\u25A1", end="   ")
        for column_number in range(10):
            print(column_number, end="   ")
        print("\n", end="")
        for row_number, row in zip(range(10), field.values()):
            print(row_number, " ", "   ".join(row))

    def _validate_ships_number(self) -> None:
        if len(self.ship_instances) != 10:
            self.print_field()
            raise IncorrectDataInput(
                "The total number of the ships should be 10"
            )

    def _validate_type_ship_quantity(self) -> None:
        allowed_ships_quantity = {4: 1, 3: 2, 2: 3, 1: 4}
        for ship in self.ship_instances:
            if len(ship.decks) in allowed_ships_quantity:
                allowed_ships_quantity[len(ship.decks)] -= 1
            else:
                raise IncorrectDataInput(
                    f"len of {ship}({len(ship.decks)} cells) is not allowed)"
                )
        for ship_type, allowed_quantity in allowed_ships_quantity.items():
            if allowed_quantity < 0:
                self.print_field()
                raise IncorrectDataInput(
                    f"Allowed quantity for {ship_type}-decks ship is"
                    f" {list(allowed_ships_quantity.keys())[ship_type - 1]}"
                )
            elif allowed_quantity > 0:
                self.print_field()
                raise IncorrectDataInput(
                    f"You've not located {allowed_quantity} of"
                    f" {ship_type}-decks ship"
                )

    def _validate_not_next_to_others(self) -> None:
        nearby_spaces = []
        for ship in self.ship_instances:
            nearby_space = []
            if ship.start_row == ship.end_row:
                for column in range(
                    ship.start_column - 1, ship.end_column + 2
                ):
                    nearby_space += [
                        (ship.start_row - 1, column),
                        (ship.start_row + 1, column),
                    ]
                nearby_spaces += nearby_space + [
                    (ship.start_row, ship.start_column - 1),
                    (ship.start_row, ship.end_column + 1),
                ]
            else:
                for row in range(ship.start_row - 1, ship.end_row + 2):
                    nearby_space += [
                        (row, ship.start_column - 1),
                        (row, ship.end_column + 1),
                    ]
                nearby_spaces += nearby_space + [
                    (ship.start_row - 1, ship.start_column),
                    (ship.end_row + 1, ship.start_column),
                ]

            for deck in ship.decks:
                if (deck.row, deck.column) in set(nearby_spaces):
                    self.print_field()
                    raise IncorrectDataInput(f"{ship} located in wrong way")

    def _validate_field(self) -> None:
        self._validate_not_next_to_others()
        self._validate_type_ship_quantity()
        self._validate_ships_number()
