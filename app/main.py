class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start_row, self.start_column = start
        self.end_row, self.end_column = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.end_row - self.start_row > 0:
            for i in range(self.start_row, self.end_row + 1):
                self.decks.append(Deck(i, self.start_column))
        else:
            for i in range(self.start_column, self.end_column + 1):
                self.decks.append(Deck(self.start_row, i))

    def get_deck(self, row: int, column: int) -> tuple | None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return row, column
        return

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                deck.is_alive = False
                break
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple[tuple]) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            deck = self.field[ship].get_deck(location[0], location[1])
            if deck:
                self.field[ship].fire(deck[0], deck[1])
                if self.field[ship].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
