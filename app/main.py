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
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def get_deck(self,
                 row: int,
                 column: int,
                 ) -> None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self,
             row: int,
             column: int,
             ) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self._validate_data = [[], []]
        self.field = {}
        self.fill_the_field(ships)
        self._validate_field()

    def _validate_field(self) -> None:
        if [1, 1, 1, 1, 2, 2, 2, 3, 3, 4] != sorted(self._validate_data[0]):
            raise ValueError("Invalid ship counts")

        matrix = self.print_field(1)
        matrix.insert(0, ["~" for _ in range(10)])
        matrix.append(["~" for _ in range(10)])

        for i_row, row in enumerate(matrix[1:11]):
            for i_col, col in enumerate(row[:11]):
                if col == "□":
                    ship = self.field[i_row, i_col]
                    decks = [(deck.row, deck.column) for deck in ship.decks]
                    for x_point, y_point in ((i_row, -~i_col),
                                             (-~i_row, -~i_col),
                                             (-~i_row, i_col),
                                             (~-i_row, -~i_col)):
                        if (x_point < 10 and y_point < 10
                                and matrix[-~x_point][y_point] == "□"
                                and (x_point, y_point) not in decks):
                            raise ValueError("Invalid ship location")

    def fill_the_field(self, ships: list) -> None:
        for ship, coordinate in enumerate(ships):
            ship = Ship(*coordinate)
            self._validate_data[1].append(ship)
            (x_aft, y_aft), (x_stern, y_stern) = coordinate
            self.field[x_stern, y_stern] = ship
            ship.decks.append(Deck(x_stern, y_stern))

            if x_aft != x_stern:
                self._validate_data[0].append(abs(x_aft - x_stern) + 1)
                x_aft, x_stern = sorted((x_aft, x_stern))
                for pos in range(x_aft, x_stern):
                    self.field[pos, y_aft] = ship
                    ship.decks.append(Deck(pos, y_aft))
            elif y_aft != y_stern:
                self._validate_data[0].append(abs(y_aft - y_stern) + 1)
                y_aft, y_stern = sorted((y_aft, y_stern))
                for pos in range(y_aft, y_stern):
                    self.field[x_aft, pos] = ship
                    ship.decks.append(Deck(x_aft, pos))
            else:
                self._validate_data[0].append(1)

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self, get_matrix: int = 0) -> list | None:
        matrix = []
        for row in range(10):
            line = []
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[row, column]
                    if ship.is_drowned:
                        line.append("x")
                        continue
                    if ship.get_deck(row, column).is_alive:
                        line.append("□")
                    else:
                        line.append("*")
                else:
                    line.append("~")
            line.append("~")
            matrix.append(line)
        if get_matrix:
            return matrix
        for row in matrix:
            print(*row[:-1])
