class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.decks = self.generate_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def get_decks(self) -> list:
        return self.decks

    def fire(self, row: int, column: int) -> bool:
        self.get_deck(row, column).is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                return True
        return False

    @staticmethod
    def generate_decks(start: int, end: int) -> list:
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            return [Deck(x1, y) for y in range(y1, y2 + 1)]
        if y1 == y2:
            return [Deck(x, y1) for x in range(x1, x2 + 1)]


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = self.generate_field(ships)
        self.field_repr = self.generate_field_representation()

    def fire(self, location: tuple) -> str:
        x, y = location

        if f"{location}" not in self.field:
            return "Miss!"

        if self.field[f"{location}"].fire(x, y):
            self.field_repr[x][y] = "*"
            return "Hit!"

        for deck in self.field[f"{location}"].get_decks():
            self.field_repr[deck.row][deck.column] = "x"

        return "Sunk!"

    def print_field(self) -> None:
        for row in self.field_repr:
            print("     ".join(row))

    @staticmethod
    def generate_field(ships: list) -> dict:
        ships = [Ship(start, end) for start, end in ships]
        decks = [ship.get_decks() for ship in ships]

        field = {
            f"{coord}": ship
            for deck, ship in zip(decks, ships)
            for coord in deck
        }
        return field

    def generate_field_representation(self) -> list:
        matrix = [["~" for _ in range(10)] for _ in range(10)]

        coordinates = [
            tuple(map(int, coord.strip("()").split(", ")))
            for coord in self.field.keys()
        ]

        for _x, _y in coordinates:
            matrix[_x][_y] = u"\u25A1"

        return matrix
