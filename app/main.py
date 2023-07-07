class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        return [Deck(row, column)
                for row in range(self.start[0], self.end[0] + 1)
                for column in range(self.start[1], self.end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        alive_decks = [deck for deck in self.decks if deck.is_alive]
        if not alive_decks:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    field = [["~" for _ in range(10)] for _ in range(10)]

    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for row in range(start[0], end[0] + 1):
                for col in range(start[1], end[1] + 1):
                    self.field[(row, col)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(location[0], location[1])

        Battleship.field[location[0]][location[1]] = "*"
        return "Miss!"

    def print_field(self) -> None:
        ships = [value for value in self.field.values()]
        for ship in ships:
            for deck in ship.decks:
                if deck.is_alive:
                    Battleship.field[deck.row][deck.column] = "\u25A1"
                if deck.is_alive is False:
                    Battleship.field[deck.row][deck.column] = "x"
        for row in Battleship.field:
            print(" ".join(row))
        print()
