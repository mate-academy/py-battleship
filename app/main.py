class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.deck = [row, column]
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
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> (None, Deck):
        for deck in self.decks:
            if deck.deck == [row, column]:
                return deck

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        if any(deck.is_alive for deck in self.decks) is True:
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {(ship[0], ship[1]): Ship(ship[0], ship[1])
                      for ship in ships}

    def fire(self, location: tuple) -> str:
        for key in self.field.keys():
            if (
                    key[0][0] <= location[0] <= key[1][0]
                    and key[0][1] <= location[1] <= key[1][1]):
                return self.field[key].fire(*location)
        return "Miss!"
