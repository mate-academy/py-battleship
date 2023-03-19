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
            self, start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                return


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
