class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_deck()

    def get_deck(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        self.check_alive()

    def check_alive(self) -> None:
        alive = any(deck.is_alive for deck in self.decks)
        if not alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple) -> str:
        for _, ship in self.field.items():
            for deck in ship.decks:
                if deck.row == location[0] and deck.column == location[1]:
                    ship.fire(location[0], location[1])
                    if not ship.is_drowned:
                        return "Hit!"
                    return "Sunk!"
        return "Miss!"
