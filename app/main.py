class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        else:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:

        if location not in self.field:
            return "Miss!"

        row, column = location
        ship = self.field[location]
        deck = ship.get_deck(row, column)

        if deck is None or not deck.is_alive:
            return "Miss!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
