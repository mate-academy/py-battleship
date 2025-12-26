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


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple
    ) -> None:
        self.decks = []
        self.is_drowned = False

        if start[0] == end[0]:
            for column in range(min(start[1], end[1]),
                                max(start[1], end[1]) + 1):
                self.decks.append(Deck(start[0], column))
        elif start[1] == end[1]:
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, start[1]))
        else:
            raise ValueError(
                "Ships must be placed either horizontally or vertically")

    def get_deck(self, row: int, column: int) -> list | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError("Overlapping ships are not allowed")
                self.field[(deck.row, deck.column)] = ship
            self.ships.append(ship)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        grid = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                match (deck.is_alive, ship.is_drowned):
                    case (False, True):
                        symbol = "x"
                    case (False, False):
                        symbol = "*"
                    case (True, _):
                        symbol = "□"
                grid[deck.row][deck.column] = symbol

        for row in grid:
            print("\t".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships")

        lengths = [len(ship.decks) for ship in self.ships]
        if lengths.count(1) != 4 or lengths.count(2) != 3 or \
           lengths.count(3) != 2 or lengths.count(4) != 1:
            raise ValueError("Incorrect number of ships by length")

        occupied = set(self.field.keys())

        for row, column in occupied:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == dy == 0:
                        continue
                    adj = (row + dx, column + dy)
                    if (
                        adj in occupied
                        and self.field[adj] != self.field[(row, column)]
                    ):
                        raise ValueError("Ships cannot touch each other")
