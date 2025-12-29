class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        hit_deck = self.get_deck(row, column)
        if hit_deck is None:
            return False  # Miss
        hit_deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
        return True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for element in ships:
            ship = Ship(element[0], element[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        else:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if not ship.is_drowned:
                return "Hit!"
            else:
                return "Sunk!"
