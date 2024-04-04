class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int],
                 end: tuple[int, int], is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for new_deck in self.decks:
            if new_deck.row == row and new_deck.column == column:
                return new_deck

    def fire(self, row: int, column: int) -> None:
        new_deck = self.get_deck(row, column)
        if new_deck and new_deck.is_alive:
            new_deck.is_alive = False
            if all(not square.is_alive for square in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int]]]) -> None:
        self.battlefield = {}
        for start, end in ships:
            ship = Ship(start, end)
            for new_ship_deck in ship.decks:
                self.battlefield[(new_ship_deck.row,
                                  new_ship_deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.battlefield:
            ship = self.battlefield[location[0], location[1]]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
