class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_coords(self) -> tuple:
        return self.row, self.column,


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = [Deck(x, y)
                      for x in range(start[0], end[0] + 1)
                      for y in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.get_coords() == (row, column):
                return deck
        raise ValueError

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = all([not deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(*ship)
            for coords in new_ship.decks:
                self.field[coords.get_coords()] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            damaged_ship = self.field[location]
            damaged_ship.fire(*location)
            if damaged_ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
