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
        self.decks = []
        self.is_drowned = is_drowned

        row1, col1 = start
        row2, col2 = end

        if row1 == row2:
            for col in range(min(col1, col2), max(col1, col2) + 1):
                self.decks.append(Deck(row1, col, True))
        elif col1 == col2:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, col1, True))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                deck.is_alive = False
                break

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = []

        for ship in ships:
            ship_obj = Ship(ship[0], ship[1])
            self.ships.append(ship_obj)

        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if not ship:
            return "Miss!"

        ship.fire(location[0], location[1])
        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for col in range(10):
                coord = (row, col)
                ship = self.field.get(coord)
                if not ship:
                    line += "~"
                else:
                    deck = ship.get_deck(row, col)
                    if not deck.is_alive and not ship.is_drowned:
                        line += "*"
                    elif ship.is_drowned:
                        line += "x"
                    else:
                        line += "□"
            print(line)
