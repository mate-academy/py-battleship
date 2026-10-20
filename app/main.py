class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for col_idx in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col_idx))
        else:
            for row_idx in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row_idx, c1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False

            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        self.ships: list[Ship] = []

        for ship_coords in ships:
            start, end = ship_coords
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row_idx, col_idx = location

        deck = ship.get_deck(row_idx, col_idx)
        if not deck or not deck.is_alive:
            return "Miss!"

        ship.fire(row_idx, col_idx)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
