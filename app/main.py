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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        # Create decks and save them to a list `self.decks`

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        check_deck_on_fire = self.get_deck(row, column)
        if check_deck_on_fire:
            check_deck_on_fire.is_alive = False
        if any([deck.is_alive for deck in self.decks]):
            self.is_drowned = False
        else:
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple]
    ) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field()
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

    def fire(self, location: tuple) -> str:
        deck_on_fire = self.field.get(location)
        if deck_on_fire:
            deck_on_fire.fire(location[0], location[1])
            if deck_on_fire.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

    @staticmethod
    def print_deck(ship: Ship, row: int, column: int) -> str:
        if ship.is_drowned:
            return "    x"
        if ship.get_deck(row, column).is_alive:
            return u"    \u25A1"
        return "    *"

    def print_field(self) -> None:
        for row in range(10):
            new_string = ""
            for column in range(10):
                ship = self.field.get((row, column))
                if ship:
                    new_string += self.print_deck(ship, row, column)
                else:
                    new_string += "    ~"
            print(f"{new_string}\n")

    def check_deck(self, test_1_deck: tuple, test_2_deck: tuple) -> None:
        if (
                test_1_deck != test_2_deck
        ) and (
                self.field[test_1_deck] != self.field[test_2_deck]
        ):
            if (
                    abs(test_1_deck[0] - test_2_deck[0]) < 2
            ) and (
                    abs(test_1_deck[1] - test_2_deck[1]) < 2
            ):
                raise (
                    ValueError("Ships shouldn't be located "
                               "in the neighboring cells")
                )

    def check_quantity_each_ship(self) -> None:
        check_number_of_ships = {
            1: ["single_deck", 4, 0],
            2: ["double_deck", 3, 0],
            3: ["three_deck", 2, 0],
            4: ["four_deck", 1, 0]
        }
        for ship in set(self.field.values()):
            ship_deck = len(ship.decks)
            check_number_of_ships[ship_deck][2] += 1
        for key in check_number_of_ships:
            if check_number_of_ships[key][2] != check_number_of_ships[key][1]:
                if key != 4:
                    raise ValueError(f"There should be "
                                     f"{check_number_of_ships[key][1]} "
                                     f"{check_number_of_ships[key][0]} ships")
                raise ValueError(f"There should be "
                                 f"{check_number_of_ships[key][1]} "
                                 f"{check_number_of_ships[key][0]} ship")

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError(f"The quantity of ships should be equal 10,"
                             f" not {len(self.field)}")
        self.check_quantity_each_ship()
        ship_coordinates = self.field.keys()
        for test_1_deck in ship_coordinates:
            for test_2_deck in ship_coordinates:
                self.check_deck(test_1_deck, test_2_deck)
