class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            row = self.start[0]
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(row, col))
        elif self.start[1] == self.end[1]:  # Vertical ship
            col = self.start[1]
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, col))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []
        self._validate_field(ships)  # Validate the ship placements
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    @staticmethod
    def _validate_field(ships: list) -> None:
        field = [[0] * 10 for _ in range(10)]

        # Place ships and check overlap
        for start, end in ships:
            if start[0] == end[0]:  # Horizontal ship
                row = start[0]
                for col in range(start[1], end[1] + 1):
                    if field[row][col] != 0:
                        raise ValueError("Ships cannot overlap or touch.")
                    field[row][col] = 1
            elif start[1] == end[1]:  # Vertical ship
                col = start[1]
                for row in range(start[0], end[0] + 1):
                    if field[row][col] != 0:
                        raise ValueError("Ships cannot overlap or touch.")
                    field[row][col] = 1

        # Check neighboring cells
        for row in range(10):
            for col in range(10):
                if field[row][col] == 1:
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            nr, nc = row + dr, col + dc
                            if (0 <= nr < 10 and 0 <= nc < 10
                                    and field[nr][nc] == 1):
                                if (dr, dc) != (0, 0) and field[nr][nc] != 2:
                                    field[nr][nc] = 2  # Mark as neighboring

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) in self.field:
            ship = self.field[(row, column)]
            return ship.fire(row, column)
        return "Miss!"
