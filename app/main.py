class Deck:
    def __init__(self, row: int, column: int, is_alive=True) -> None:
        self.deck = [row, column]
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> (None, Deck):
        for deck in self.decks:
            if deck.deck == [row, column]:
                return deck

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        print([deck.is_alive for deck in self.decks])
        if any(deck.is_alive for deck in self.decks) is True:
            return "Hit!"
        self.is_drowned = False
        return "Sunk!"


class Battleship:
    def __init__(self, ships) -> None:
        self.field = {(ship[0], ship[1]): Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for k, v in self.field.items():
            if k[0][0] <= location[0] <= k[1][0] and k[0][1] <= location[1] <= k[1][1]:
                return self.field[k].fire(*location)
        return "Miss!"
