class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.decks = {}
        self.is_drowned = is_drowned
        self.create_deckds()

    def get_deck(self, row: int, column: int) -> Deck | None:
        deck = (row, column)
        if deck in self.decks:
            return self.decks[(row, column)]

    def create_deckds(self) -> None:
        if self.start[0] == self.end[0]:
            for row in range(self.start[1], self.end[1] + 1):
                self.decks[(self.start[0], row)] = (Deck(self.start[0], row))
        elif self.start[1] == self.end[1]:
            for column in range(self.start[0], self.end[0] + 1):
                self.decks[(column, self.end[1])] = (Deck(column, self.end[1]))

    def fire(self, row: int, column: int) -> str:
        current_deck = self.get_deck(row, column)
        if current_deck is None:
            return "Miss!"
        if current_deck.is_alive is False and self.is_drowned is False:
            return "Miss!"
        if current_deck.is_alive is True:
            current_deck.is_alive = False
        result = 0
        for deck in self.decks.values():
            if deck.is_alive:
                result += 1
        if result == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        self.create_ship()

    def create_ship(self) -> None:
        for ship in self.ships:
            if ship[0][0] == ship[1][0]:
                row_key = []
                for row in range(ship[0][1], ship[1][1] + 1):
                    row_key.append((ship[0][0], row))
                self.field[tuple(row_key)] = Ship(ship[0], ship[1])
            elif ship[0][1] == ship[1][1]:
                column_key = []
                for column in range(ship[0][0], ship[1][0] + 1):
                    column_key.append((column, ship[0][1]))
                self.field[tuple(column_key)] = Ship(ship[0], ship[1])

    def fire(self, location: tuple) -> str:
        for coords, ship in self.field.items():
            if location in coords:
                return ship.fire(location[0], location[1])
        return "Miss!"
