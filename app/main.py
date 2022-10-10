class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.check_if_drowned()

    def check_if_drowned(self) -> None:
        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                return


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}

        for ship in ships:
            battle_ship = Ship(*ship)
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        self.field[location].fire(*location)

        if self.field[location].is_drowned:
            return "Sunk!"

        return "Hit!"
