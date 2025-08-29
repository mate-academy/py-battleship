from collections import Counter


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.create_decks(start, end)

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list:
        start_row, start_col = start
        end_row, end_col = end
        decks = []
        if start_row == end_row:
            for col in range(
                    min(start_col, end_col), max(start_col, end_col) + 1
            ):
                decks.append(Deck(start_row, col))
        elif start_col == end_col:
            for row in range(
                    min(start_row, end_row), max(start_row, end_row) + 1
            ):
                decks.append(Deck(row, start_col))
        else:
            raise ValueError("Ship must be placed vertically or horizontally")
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is None:
            return False
        if not deck.is_alive:
            return False
        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
        return True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        row, col = location
        deck = ship.get_deck(row, col)
        if deck is None or not deck.is_alive:
            return "Miss!"
        ship.fire(row, col)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of ships must be 10.")
        sizes = Counter(len(ship.decks) for ship in self.ships)
        required = {1: 4, 2: 3, 3: 2, 4: 1}
        for size, req_count in required.items():
            if sizes.get(size, 0) != req_count:
                raise ValueError(
                    "Invalid ship distribution: expected "
                    "4×1, 3×2, 2×3, 1×4 deck ships."
                )
        unexpected = [s for s in sizes if s not in required]
        if unexpected:
            raise ValueError(f"Unexpected ship sizes present: {unexpected}")
        total_decks = sum(len(ship.decks) for ship in self.ships)
        if len(self.field) != total_decks:
            raise ValueError("Ships overlap on the field.")
        neighbors = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
        for ship in self.ships:
            for deck in ship.decks:
                r, c = deck.row, deck.column
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    other = self.field.get((nr, nc))
                    if other is not None and other is not ship:
                        raise ValueError("Ships must not be adjacent (even diagonally).")
