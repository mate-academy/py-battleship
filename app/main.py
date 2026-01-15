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

        start_x, start_y = start
        end_x, end_y = end

        self.decks = [Deck(i, j)
                      for i in range(start_x, end_x + 1)
                      for j in range(start_y, end_y + 1)]

        self.ship_set = set((i, j)
                            for i in range(start_x, end_x + 1)
                            for j in range(start_y, end_y + 1))

        buf_start_x, buf_start_y = max(0, start[0] - 1), max(0, start[1] - 1)
        buf_end_x, buf_end_y = (min(9, end[0] + 1), min(9, end[1] + 1))

        self.buffer_set = (set((i, j)
                               for i in range(buf_start_x, buf_end_x + 1)
                               for j in range(buf_start_y, buf_end_y + 1))
                           - self.ship_set)

    def __len__(self) -> int:
        return len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for x_coord in range(start[0], end[0] + 1):
                for y_coord in range(start[1], end[1] + 1):
                    self.field[(x_coord, y_coord)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        expected_ships = {1: 4, 2: 3, 3: 2, 4: 1}

        if len(self.ships) != 10:
            raise ValueError("the total number of the ships should be 10")

        real_ships = {}

        for ship in self.ships:
            real_ships[len(ship)] = real_ships.get(len(ship), 0) + 1

        if sorted(expected_ships) != sorted(real_ships):
            raise ValueError("4 single-deck ships, 3 double-deck ships, "
                             "2 three-deck ships, 1 four-deck ship expected")

        inhabited_set = set()

        for ship in self.ships:
            if ship.ship_set & inhabited_set:
                raise ValueError("ships shouldn't be located "
                                 "in the neighboring cells")
            inhabited_set |= ship.ship_set
            inhabited_set |= ship.buffer_set
