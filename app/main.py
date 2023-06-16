class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        pass


class Ship:
    def __init__(self,
                 start: tuple, end: tuple, is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [Deck(row, column)
                      for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.column == column and deck.row == row:
                return deck
        raise ValueError("We haven't deck with params")

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)

    def ship_print(self, row: int, column: int) -> str:
        if self.is_drowned:
            return "x"
        else:
            return u"\u25A1" if self.get_deck(row, column).is_alive else "*"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = dict()

        for ship in self.ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> list:
        matrix = [["~" if (row, column) not in self.field
                   else self.field[(row, column)].ship_print(row, column)
                   for column in range(0, 10)] for row in range(0, 10)]
        for row in matrix:
            print(" ".join(row))
        return matrix
