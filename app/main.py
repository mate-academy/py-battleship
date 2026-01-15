class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_coordinates(self) -> tuple:
        return self.row, self.column

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()
        self.is_drowned = is_drowned

    def create_decks(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.get_coordinates() == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.hit()
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = [["~"] * 10 for _ in range(10)]

    def place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "□"

    def fire(self, location: tuple) -> str:
        row, column = location
        for ship in self.ships:
            result = ship.fire(row, column)
            if result == "Hit!" or result == "Sunk!":
                self.field[row][column] = "x"
                return result
        self.field[row][column] = "o"
        return "Miss!"
