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

        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], index)
                for index in range(start[1], end[1] + 1)]
        else:
            self.decks = [
                Deck(j, start[1])
                for j in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for index in self.decks:
            if index.column == column and index.row == row:
                return index

    def fire(self, row: int, column: int) -> None:
        is_any_alive = False
        got_hit = False
        for index in self.decks:
            if index.column == column and index.row == row:
                index.is_alive = False
                got_hit = True
        for deck in self.decks:
            if deck.is_alive is True:
                is_any_alive = True
        if got_hit and not is_any_alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = (deck, ship)

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        deck, ship = self.field[location]
        deck.is_alive = False
        ship.fire(deck.row, deck.column)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
