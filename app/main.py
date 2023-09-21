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
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.decks = []
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = []

        for ship in ships:
            created_ship = Ship(ship[0], ship[1])
            self.ships.append(created_ship)
            self._place_ship_on_field(created_ship)

    def _place_ship_on_field(self, ship: Ship) -> None:
        for deck in ship.decks:
            self.field[deck.row][deck.column] = u"\u25A1"

    def fire(self, cell: tuple[int, int]) -> str:
        row, col = cell
        if self.field[row][col] == u"\u25A1":
            self.field[row][col] = "x"
            for ship in self.ships:
                result = ship.fire(row, col)
                if result == "Sunk!":
                    return "Sunk!"
                elif result == "Hit!":
                    return "Hit!"
            return "Miss!"
        elif self.field[row][col] == "~":
            self.field[row][col] = "*"
            return "Miss!"
        else:
            return "Already fired here."
