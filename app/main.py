class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row=self.start[0], column=self.start[1] + el)
            if self.start[0] == self.end[0]
            else Deck(row=self.start[0] + el, column=self.start[1])
            for el in range(abs((self.start[0] - self.end[0])
                                + (self.start[1] - self.end[1])) + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck is None:
            return "Miss"

        if not deck.is_alive:
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"

        deck.is_alive = False

        if not any(d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship_coords in ships:
            ship = Ship(start=ship_coords[0], end=ship_coords[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = (deck, ship)

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        deck, ship = self.field[location]

        if not deck.is_alive:
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"

        deck.is_alive = False

        if not any(d.is_alive for d in ship.decks):
            ship.is_drowned = True
            return "Sunk!"

        return "Hit!"
