class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: list, end: list,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        r_start, c_start = start
        r_end, c_end = end

        row_step = 1 if r_end > r_start else -1 if r_end < r_start else 0
        col_step = 1 if c_end > c_start else -1 if c_end < c_start else 0
        self.length = max(abs(r_end - r_start), abs(c_end - c_start)) + 1

        for i in range(self.length):
            row = r_start + i * row_step
            column = c_start + i * col_step
            self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(s[0], s[1]) for s in ships]
        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        lengths = sorted([ship.length for ship in self.ships])
        if lengths != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError
        occupied_coords = list(self.field.keys())
        for i, (row, column) in enumerate(occupied_coords):
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    neighbor = (row + dr, column + dc)
                    if (neighbor in self.field
                            and self.field[neighbor]
                            != self.field[(row, column)]):
                        raise ValueError

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
