class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if any([deck.is_alive for deck in self.decks]) is False:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for start, end in ships:
            cords = [
                (row, column)
                for row in range(start[0], end[0] + 1)
                for column in range(start[1], end[1] + 1)]
            ship = Ship(start, end)
            for cord in cords:
                self.field[cord] = ship
        self._validate_input(ships)

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship:
            ship.fire(*location)
            if ship.is_drowned is True:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(9 + 1):
            for column in range(9 + 1):
                ship = self.field.get((row, column))
                if ship:
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        print(" X ", end="")
                        continue
                    elif deck.is_alive:
                        print(u" \u25A1 ", end="")
                    else:
                        print(" * ", end="")
                else:
                    print(" ~ ", end="")
            print("")

    def _validate_input(self, ships: list[tuple]) -> None:
        # Check if count of ships == 10
        if len(ships) < 10:
            raise ValueError(f"Count of ships should be"
                             f"equal 10, got {len(ships)} instead")
        count_of_ships = {1: 0, 2: 0, 3: 0, 4: 0, }
        list_of_ships = list(self.field.values())
        # Counting each ship type, and adding it to dict
        for ship in set(list_of_ships):
            count_of_ships[list_of_ships.count(ship)] += 1
        # Checking if there is correct count of each ship type
        if ([count_of_ships[1], count_of_ships[2],
             count_of_ships[3], count_of_ships[4]] != [4, 3, 2, 1]):
            raise ValueError(f"There should be: \n"
                             f"4 one-deck ships, "
                             f"got {count_of_ships[1]} instead\n"
                             f"3 double-deck ships, "
                             f"got {count_of_ships[2]} instead\n"
                             f"2 three-deck ships, "
                             f"got {count_of_ships[3]} instead\n"
                             f"1 four-deck ship, "
                             f"got {count_of_ships[4]} instead")
        # Checking if there ships in neighboring cells
        for cord, ship in self.field.items():
            for row in range(cord[0] - 1, cord[0] + 2):
                for column in range(cord[1] - 1, cord[1] + 2):
                    self._check_ceil(row, column, ship)

    def _check_ceil(self, row: int, column: int, ship: Ship) -> None:
        if (self.field.get((row, column))
                and self.field.get((row, column)) != ship):
            raise ValueError("Ships cannot be in neighboring cells"
                             "(even if cells are neighbors by diagonal)")
