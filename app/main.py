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
            self.field[ship] = Ship(*ship)

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            if location[0] == ship[0][0]:
                if ship[0][1] <= location[1] <= ship[1][1]:
                    self.field[ship].fire(*location)
                    if self.field[ship].is_drowned:
                        return "Sunk!"
                    return "Hit!"
            elif location[1] == ship[0][1]:
                if ship[0][0] <= location[0] <= ship[1][0]:
                    self.field[ship].fire(*location)
                    if self.field[ship].is_drowned:
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"
