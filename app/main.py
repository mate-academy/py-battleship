class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

    @property
    def decks(self) -> list:
        if not hasattr(self, "_decks"):
            row_start, col_start = self.start
            row_end, col_end = self.end
            col_start, col_end = (
                min(col_start, col_end),
                max(col_start, col_end)
            )
            row_start, row_end = (
                min(row_start, row_end),
                max(row_start, row_end)
            )
            if row_start == row_end:
                self._decks = [
                    Deck(row_start, i)
                    for i in range(col_start, col_end + 1)
                ]
            else:
                self._decks = [
                    Deck(i, col_start)
                    for i in range(row_start, row_end + 1)
                ]
        return self._decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
        else:
            return "Already destroyed!"
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.ships = ships
        self.field = {}
        for ship_ in ships:
            ship = Ship(ship_[0], ship_[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if not ship.is_drowned and deck.is_alive:
                        print("□", end="\t")
                        continue
                    if not ship.is_drowned and not deck.is_alive:
                        print("*", end="\t")
                        continue
                    if ship.is_drowned:
                        print("x", end="\t")
                        continue
                print("~", end="\t")
            print()
