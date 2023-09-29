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
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list:
        start_row, start_column = start
        end_row, end_column = end
        if start == end:
            return [Deck(start_row, start_column)]
        elif start_row == end_row:
            return [
                Deck(start_row, column)
                for column in range(start_column, end_column + 1)
            ]
        elif start_column == end_column:
            return [
                Deck(row, start_column)
                for row in range(start_row, end_row + 1)
            ]

    def check_is_drowned(self) -> bool:
        ship_is_drowned = all(deck.is_alive is False for deck in self.decks)
        if ship_is_drowned:
            return True
        return False

    def get_deck(self, row: tuple, column: tuple) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: tuple, column: tuple) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if self.check_is_drowned():
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.battleground = self.create_battleground()
        self.field = self.ships_placement(ships)

    def ship_mark(self, deck: Deck) -> None:
        self.battleground[deck.row][deck.column] = u"\u25A1"

    def ships_placement(self, ships: list) -> dict:
        field = self.create_field()
        for ship in ships:
            start, end = ship
            ship = Ship(start, end)
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
                self.ship_mark(deck)
        return field

    @staticmethod
    def create_field() -> dict:
        field = {}
        rows, columns = 10, 10
        for row in range(rows):
            for col in range(columns):
                field[(row, col)] = None
        return field

    @staticmethod
    def create_battleground() -> list:
        return [["~"] * 10 for _ in range(10)]

    def print_battleground(self) -> None:
        for row in self.battleground:
            print("    ".join(row))

    def hit_deck(self, row: int, column: int) -> str:
        self.battleground[row][column] = "*"
        return "Hit!"

    def sunk_ship(self, ship: Ship) -> str:
        for deck in ship.decks:
            self.battleground[deck.row][deck.column] = "x"
        return "Sunk!"

    def fire(self, location: tuple) -> str:
        ship = self.field[location]
        if not ship:
            return "Miss!"

        row, column = location
        action = ship.fire(row, column)

        if action == "Hit!":
            return self.hit_deck(row, column)
        elif action == "Sunk!":
            return self.sunk_ship(ship)
