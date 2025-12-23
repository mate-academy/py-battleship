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

        self.decks = []
        self.is_drowned = is_drowned
        if start[0] == end[0] and start[1] != end[1]:
            for deck in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], deck))
        elif start[1] == end[1] and start[0] != end[0]:
            for deck in range(start[0], end[0] + 1):
                self.decks.append(Deck(deck, start[1]))
        else:
            self.decks.append(Deck(start[0], end[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        count = 0
        for deck in self.decks:
            if not deck.is_alive:
                count += 1
        if count == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {coord: Ship(*coord) for coord in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
