class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.decks = [
            Deck(row, column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if self.get_deck(row, column) == deck:
                deck.is_alive = False
                if any(decks.is_alive for decks in self.decks) is False:
                    return "Sunk!"
                return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = []
        self.field = {}
        for deck in ships:
            self.ships.append(Ship(deck[0], deck[1]))
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        for coordinates in self.field:
            if coordinates == location:
                return self.field[coordinates].fire(location[0], location[1])
        return "Miss!"
