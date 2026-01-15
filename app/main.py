class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int],
                 end: tuple[int], is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = [Deck(row, column)
                      for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
        if all(not deck.is_alive for deck in self.decks):
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for key, ship in self.field.items():
            if (key[0][0] <= location[0] <= key[1][0]
                    and key[0][1] <= location[1] <= key[1][1]):
                return ship.fire(*location)
        return "Miss!"
