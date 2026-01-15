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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = self._create_field()
        self._validate_field()

    def _create_field(self) -> dict:
        field = {}
        for ship in self.ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def _validate_field(self) -> None:
        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            length = len(ship.decks)
            if length > 4:
                raise ValueError("Invalid ship size.")
            counts[length] += 1
        if counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid ship distribution.")

        all_cells = set(self.field.keys())
        for ship in self.ships:
            ship_cells = {(deck.row, deck.column) for deck in ship.decks}
            for cell in ship_cells:
                row, col = cell
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        neighbor = (row + dr, col + dc)
                        if (neighbor in all_cells
                                and neighbor not in ship_cells):
                            raise ValueError(
                                "Ships are too close to each other."
                            )

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row, col = location
        if ship.fire(row, col):
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
