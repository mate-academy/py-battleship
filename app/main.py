class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> list | str:
        (r1, c1), (r2, c2) = self.start, self.end

        if r1 == r2:
            start, end = sorted([c1, c2])
            return [Deck(r1, c) for c in range(start, end + 1)]

        if c1 == c2:
            start, end = sorted([r1, r2])
            return [Deck(r, c1) for r in range(start, end + 1)]

        raise ValueError

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None | str:
        deck = self.get_deck(row, column)
        if deck is None:
            return None

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str | Ship:
        row, col = location

        if (row, col) not in self.field:
            return "Miss!"

        ship = self.field[(row, col)]
        return ship.fire(row, col)
