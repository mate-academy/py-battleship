class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:

        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:

        if start == end:
            self.decks = [Deck(*start)]
        if start[1] < end[1]:
            self.decks = [Deck(start[0], end_)
                          for end_ in range(start[1], end[1] + 1)]
        if start[0] < end[0]:
            self.decks = [Deck(start_, start[1])
                          for start_ in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self,
                 row: int,
                 column: int) -> int:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return self.decks.index(deck)

    def fire(self,
             row: int,
             column: int) -> None:

        index = self.get_deck(row, column)
        self.decks[index].is_alive = False
        if all(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: Ship) -> None:
        self.field = {}
        for coordinate in ships:
            ship = Ship(*coordinate)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            ship = self.field.get(location)
            if sum(map(lambda x: x.is_alive, ship.decks)) == 1:
                ship.fire(*location)
                return "Sunk!"
            else:
                ship.fire(*location)
                return "Hit!"
