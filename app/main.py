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
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            for y_coord in range(min(y1, y2), max(y1, y2) + 1):
                self.decks.append(Deck(x1, y_coord))
        elif y1 == y2:
            for x_coord in range(min(x1, x2), max(x1, x2) + 1):
                self.decks.append(Deck(x_coord, y1))
        else:
            raise ValueError

    def get_deck(self, row: int, column: int) -> Deck | None:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:

        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:

        self.ships = []
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self,
             location: tuple[int, int]) -> str:

        row, column = location
        ship = self.field.get((row, column))

        if not ship:
            return "Miss!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"
