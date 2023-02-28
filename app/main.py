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
                 start: tuple,
                 end: tuple,
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

    def get_deck(self, row: int, column: int) -> Deck:
        return [deck for deck in self.decks if deck.row == row
                and deck.column == column][0]

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if sum([1 for deck_ in self.decks if not
                deck_.is_alive]) == len(self.decks):
            self.is_drowned = True


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
            i, j = ship.start
            i2, j2 = ship.end
            if i == i2:
                if j > j2:
                    j, j2 = j2, j
                self._validate_horizontal_ship_position(i, j, j2)
            elif j == j2:
                if i > i2:
                    i, i2 = i2, i
                self._validate_vertical_ship_position(j, i, i2)
            else:
                raise ValueError

    def _validate_horizontal_ship_position(self,
                                           i: int,
                                           _j: int
                                           ) -> None:

        if _j == 0:
            if not all(self.field[i + di][0] == self.EMPTY_CELL
                       for di in [-1, 0, 1] if 0 <= i + di <= 9):
                raise ValueError
            if not all(self.field[i + di][1] == self.EMPTY_CELL
                       for di in [-1, 0, 1] if 0 <= i + di <= 9):
                raise ValueError
        elif _j == 9:
            if not all(self.field[i + di][9] == self.EMPTY_CELL
                       for di in [-1, 0, 1] if 0 <= i + di <= 9):
                raise ValueError
            if not all(self.field[i + di][8] == self.EMPTY_CELL
                       for di in [-1, 0, 1] if 0 <= i + di <= 9):
                raise ValueError
        else:
            if not all(self.field[i + di][_j + dj] == self.EMPTY_CELL
                       for di in [-1, 0, 1] for dj in [-1, 0, 1]
                       if 0 <= i + di <= 9 and 0 <= _j + dj <= 9):
                raise ValueError

    def _validate_vertical_ship_position(self,
                                         _j: int,
                                         i: int,
                                         i2: int
                                         ) -> None:

        if i == 0:
            if not all(self.field[0][_j + dj] == self.EMPTY_CELL
                       for dj in [-1, 0, 1] if 0 <= _j + dj <= 9):
                raise ValueError
            if not all(self.field[1][_j + dj] == self.EMPTY_CELL
                       for dj in [-1, 0, 1] if 0 <= _j + dj <= 9):
                raise ValueError
        elif i == 9:
            if not all(self.field[9][_j + dj] == self.EMPTY_CELL
                       for dj in [-1, 0, 1] if 0 <= _j + dj <= 9):
                raise ValueError
            if not all(self.field[8][_j + dj] == self.EMPTY_CELL
                       for dj in [-1, 0, 1] if 0 <= _j + dj <= 9):
                raise ValueError
        else:
            if not all(self.field[i + di][_j + dj] == self.EMPTY_CELL
                       for di in [-1, 0, 1] for dj in [-1, 0, 1] if
                       0 <= i + di <= 9 and 0 <= _j + dj <= 9):
                raise ValueError

    def print_field(self) -> None:
        for row in self.field:
            for item in row:
                print(item, end=" ")
            print()

    def _add_ship(self, start: tuple, end: tuple) -> None:
        ship = Ship(start, end)
        self.ships.append(ship)
        for deck in ship.decks:
            self.field[deck.row][deck.column] = self.SHIP_DECK

    def _get_ship(self, row: int, column: int) -> Ship:
        for ship in self.ships:
            if len(ship.decks) == 1 and row == ship.start[0] \
                    and column == ship.start[1]:
                return ship
            num = 1 if ship.start[1] == ship.end[1] else 0
            if row == ship.start[num % 2] and ship.start[(num + 1) % 2] \
                    <= column <= ship.end[(num + 1) % 2]:
                return ship

    def fire(self, location: tuple) -> str:
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
        else:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = self.DESTROYED_SHIP_DECK
            return "Sunk!"
