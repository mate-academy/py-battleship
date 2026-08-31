class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.coor = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        if start == end:
            self.decks.append(Deck(*start))
        else:
            if start[0] == end[0]:
                for deck in range(start[1], end[1] + 1):
                    self.decks.append(Deck(start[0], deck))
            elif start[1] == end[1]:
                for deck in range(start[0], end[0] + 1):
                    self.decks.append(Deck(start[1], deck))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.coor == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            for deck in ship.decks:
                self.field[deck.coor] = ship

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        pass
