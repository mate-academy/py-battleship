class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        destroyed_deck = self.get_deck(row, column)
        if destroyed_deck:
            destroyed_deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        self.fields = {}
        for ship in ships:
            self.ship = Ship(ship[0], ship[1])
            for deck in self.ship.decks:
                self.fields[deck.row, deck.column] = self.ship

    def fire(self, location: tuple) -> str:
        if location not in self.fields:
            return "Miss!"

        self.fields[location].fire(location[0], location[1])
        if self.fields[location].is_drowned:
            return "Sunk!"
        return "Hit!"
