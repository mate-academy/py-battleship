class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        row_start, column_start = start
        row_end, column_end = end
        self.decks = []
        self.is_drowned = is_drowned
        for row in range(row_start, row_end + 1):
            for column in range(column_start, column_end + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = dict()
        for ship in ships:
            start, end = ship
            each_ship = Ship(start, end)
            for deck in each_ship.decks:
                self.field[(deck.row, deck.column)] = each_ship
        self.print_field()
        self._validate_field()

    def _validate_field(self) -> None:
        set_ships = set(self.field.values())
        #  the total number of the ships should be 10
        quantity = len(set_ships)
        if quantity != 10:
            print(f"There must be 10 ships, but are {quantity}")
            return
        # should be the correct number of different ships
        ships_by_type = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship in set_ships:
            length = len(ship.decks)
            if length in ships_by_type.keys():
                ships_by_type[length] += 1
        for number_of_decks in ships_by_type:
            if number_of_decks + ships_by_type[number_of_decks] != 5:
                print(f"There must be {5 - number_of_decks} ships, "
                      f"with {number_of_decks} decks")
                return
        # ships shouldn't be located in the neighboring cells
        for ship in set_ships:
            row_start, column_start = ship.decks[0].row, ship.decks[0].column
            row_end, column_end = ship.decks[-1].row, ship.decks[-1].column
            for row in range(row_start - 1, row_end + 2):
                for column in range(column_start - 1, column_end + 2):
                    if 0 <= row <= 9 and 0 <= column <= 9:
                        if (row_start <= row <= row_end
                                and column_start <= column <= column_end):
                            continue
                        try:
                            if self.field[(row, column)]:
                                print("The ships are not positioned correctly")
                                return
                        except KeyError:
                            pass

    def fire(self, location: tuple) -> str:
        row, column = location
        try:
            if self.field[(row, column)]:
                ship = self.field[(row, column)]
                ship.fire(row, column)
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        except KeyError:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            print(" ", end="")
            for column in range(10):
                try:
                    ship = self.field[(row, column)]
                    if ship:
                        symbol = "x" if ship.is_drowned else "*"
                        if ship.get_deck(row, column).is_alive:
                            print(u"\u25A1", " ", end="")
                        else:
                            print(symbol, " ", end="")
                except KeyError:
                    print("~", " ", end="")
            print("")
