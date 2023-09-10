class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.live_decks = len(self.decks)

    def get_deck(self,
                 row: int,
                 column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self,
             row: int,
             column: int) -> None:
        wrecked_deck = self.get_deck(row, column)
        if wrecked_deck is not None:
            wrecked_deck.is_alive = False
        if all(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple[int]) -> str:
        for ship in self.field.values():
            for deck in ship.decks:
                if (deck.row, deck.column) == location:
                    deck.is_alive = False
                    ship.live_decks -= 1
                    if ship.live_decks == 0:
                        ship.is_drowned = True
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"
