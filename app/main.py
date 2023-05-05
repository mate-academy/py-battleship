class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks.append(Deck(*start))
        elif start[0] == end[0] and start[1] != end[1]:
            columns = range(start[1], end[1] + 1)
            for column in columns:
                self.decks.append(Deck(start[0], column))
        else:
            rows = range(start[0], end[0] + 1)
            for row in rows:
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for coords in ships:
            start, end = coords[0], coords[1]
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field.update({(deck.row, deck.column): ship})

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)

            all_ship_decks_destroyed = True
            for deck in ship.decks:
                if deck.is_alive:
                    all_ship_decks_destroyed = False
                    break

            if all_ship_decks_destroyed:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
