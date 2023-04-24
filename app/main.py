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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        if self.start[0] == self.end[0]:
            for col in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for ship_coord in ships:
            ship = Ship(ship_coord[0], ship_coord[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
