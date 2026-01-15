class UserError(Exception):
    pass


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
        self.is_drowned = is_drowned
        self.decks = [
            Deck(x, y) for x in range(start[0], end[0] + 1)
            for y in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any([desk.is_alive for desk in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for value in ships:
            ship = Ship(value[0], value[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field.get((row, column))
                    if ship.is_drowned:
                        print("  x  ", end="")
                    else:
                        if ship.get_deck(row, column).is_alive:
                            print(u"  \u25A1  ", end="")
                        else:
                            print("  *  ", end="")
                else:
                    print("  ~  ", end="")
            print("\n")

    def _validate_field(self) -> None:
        ships: list[Ship] = [ship for ship in self.field.values()]
        count_decks_for_ship: dict = {
            ship: ships.count(ship) for ship in ships
        }
        decks_values: list = list(count_decks_for_ship.values())
        if len(count_decks_for_ship) != 10:
            raise UserError("The total number of the ships should be 10")
        if decks_values.count(1) != 4:
            raise UserError("There should be 4 single-deck ships")
        if decks_values.count(2) != 3:
            raise UserError("There should be 3 double-deck ships")
        if decks_values.count(3) != 2:
            raise UserError("There should be 2 three-deck ships")
        if decks_values.count(4) != 1:
            raise UserError("There should be 1 four-deck ship")

        for deck1, ship1 in self.field.items():
            for deck2, ship2 in self.field.items():
                if ship1 != ship2:
                    if (abs(deck1[0] - deck2[0]) < 2
                            and abs(deck1[1] - deck2[1]) < 2):
                        raise UserError(
                            "ships shouldn't be located in the "
                            "neighboring cells (even if cells are "
                            "neighbors by diagonal)"
                        )
