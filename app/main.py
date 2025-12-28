class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.deck = []
        if start[0] == end[0]:
            for y_coord in range(start[1], end[1] + 1):
                self.deck.append(Deck(start[0], y_coord))
        elif start[1] == end[1]:
            for x_coord in range(start[0], end[0] + 1):
                self.deck.append(Deck(x_coord, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.deck:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str | None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.deck):
                return "Sunk!"
            return "Hit!"
        return None


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]
                 ) -> None:
        self.field = []
        for start, end in ships:
            self.field.append(Ship(start, end))

    def fire(self, location: tuple[int, int]) -> str:
        row, column = location
        for ship in self.field:
            result = ship.fire(row, column)
            if result is not None:
                return result
        return "Miss!"
