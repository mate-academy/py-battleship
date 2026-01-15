class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        current_deck = self.get_deck(row, column)
        if current_deck:
            current_deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) in self.field:
            ship = self.field[(row, column)]
            return ship.fire(row, column)
        return "Miss!"
