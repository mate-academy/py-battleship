class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start[1] == end[1]:

            for pos in range(start[0], end[0] + 1):
                self.decks.append(Deck(pos, start[1]))
        elif start[0] == end[0]:
            for pos in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], pos))

    def get_deck(self,
                 row: int,
                 column: int
                 ) -> Deck:

        return next(
            deck for deck in self.decks
            if deck.row == row and deck.column == column)

    def fire(self,
             row: int,
             column: int
             ) -> None:

        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    SHIP_DECK = "□"
    HIT_SHIP_DECK = "*"
    DESTROYED_SHIP_DECK = "x"
    EMPTY_CELL = "~"

    def __init__(self, ships: list[Ship]) -> None:
        self.field = [[self.EMPTY_CELL for _ in range(10)] for _ in range(10)]
        self.ships = []
        for start, end in ships:
            self._add_ship(start, end)

    def _validate_ship_sizes(self) -> None:
        ship_sizes = [len(ship.decks) for ship in self.ships]
        expected_ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        if sorted(ship_sizes) != expected_ship_sizes:
            raise ValueError

    def _validate_ship_positions(self) -> None:
        for ship in self.ships:
            row_start, col_start = ship.start
            row_end, col_end = ship.end
            if row_start == row_end:
                if col_start > col_end:
                    col_start, col_end = col_end, col_start
                self._validate_horizontal_ship_position(
                    row_start,
                    col_start,
                    col_end
                )
            elif col_start == col_end:
                if row_start > row_end:
                    row_start, row_end = row_end, row_start
                self._validate_vertical_ship_position(
                    col_start,
                    row_start,
                    row_end
                )
            else:
                raise ValueError

    def check_h_position(self, row: int, index: int) -> None:
        if not all(self.field[row + di][index] == self.EMPTY_CELL
                   for di in [-1, 0, 1] if 0 <= row + di <= 9):
            raise ValueError

    def _validate_horizontal_ship_position(self,
                                           row: int,
                                           col: int
                                           ) -> None:

        if col == 0:
            self.check_h_position(row, 0)
            self.check_h_position(row, 1)

        elif col == 9:
            self.check_h_position(row, 9)
            self.check_h_position(row, 8)
        else:
            if not all(self.field[row + di][col + dj] == self.EMPTY_CELL
                       for di in [-1, 0, 1] for dj in [-1, 0, 1]
                       if 0 <= row + di <= 9 and 0 <= col + dj <= 9):
                raise ValueError

    def check_v_position(self, col: int, index: int) -> None:
        if not all(self.field[index][col + dj] == self.EMPTY_CELL
                   for dj in [-1, 0, 1] if 0 <= col + dj <= 9):
            raise ValueError

    def _validate_vertical_ship_position(self,
                                         col: int,
                                         row: int,
                                         ) -> None:

        if row == 0:
            self.check_v_position(col, 0)
            self.check_v_position(col, 1)
        elif row == 9:
            self.check_v_position(col, 9)
            self.check_v_position(col, 8)
        else:
            if not all(self.field[row + di][col + dj] == self.EMPTY_CELL
                       for di in [-1, 0, 1] for dj in [-1, 0, 1] if
                       0 <= row + di <= 9 and 0 <= col + dj <= 9):
                raise ValueError

    def print_field(self) -> None:
        for row in self.field:
            for item in row:
                print(item, end=" ")
            print()

    def _add_ship(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        ship = Ship(start, end)
        self.ships.append(ship)
        for deck in ship.decks:
            self.field[deck.row][deck.column] = self.SHIP_DECK

    def _get_ship(self, row: int, column: int) -> Ship:
        for ship in self.ships:
            if (len(ship.decks) == 1 and row == ship.start[0]
                    and column == ship.start[1]):
                return ship
            num = 1 if ship.start[1] == ship.end[1] else 0
            if row == ship.start[num % 2] and ship.start[(num + 1) % 2] \
                    <= column <= ship.end[(num + 1) % 2]:
                return ship

    def fire(self, location: tuple[int, int]) -> str:
        x, y = location
        if not (0 <= x <= 9 and 0 <= y <= 9):
            raise ValueError

        if self.field[x][y] == self.EMPTY_CELL:
            return "Miss!"

        ship = self._get_ship(x, y)
        ship.fire(x, y)
        if not ship.is_drowned:
            self.field[x][y] = self.HIT_SHIP_DECK
            return "Hit!"
        return "Sunk!"
