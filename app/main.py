class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        (start_r, start_c), (end_r, end_c) = start, end
        for row in range(start_r, end_r + 1):
            for column in range(start_c, end_c + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        current_deck = self.get_deck(row, column)
        if current_deck is not None:
            current_deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            current_ship = Ship(*ship)
            for deck in current_ship.decks:
                self.field[deck.row, deck.column] = current_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
