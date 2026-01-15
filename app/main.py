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
        self.decks = []

        if start == end:
            self.decks.append(Deck(start[0], start[1], True))
        elif start[0] == end[0]:
            for num in range(
                    min(start[1], end[1]),
                    max(start[1], end[1]) + 1
            ):
                self.decks.append(Deck(start[0], num, True))
        elif start[1] == end[1]:
            for num in range(
                    min(start[0], end[0]),
                    max(start[0], end[0]) + 1
            ):
                self.decks.append(Deck(num, start[1], True))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        if not deck.is_alive:
            return "Miss!"
        deck.is_alive = False
        if any(deck.is_alive for deck in self.decks):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(row, column)

    def print_field(self) -> None:
        for row in range(10):
            row_symbols = []
            for column in range(10):
                if (row, column) not in self.field:
                    row_symbols.append("~")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    symbol = "x" if ship.is_drowned else "*" \
                        if not deck.is_alive else "□"
                    row_symbols.append(symbol)
            print(" ".join(row_symbols))

    def _validate_field(self) -> None:
        single_deck = 0
        double_deck = 0
        triple_deck = 0
        quad_deck = 0
        for ship in self.ships:
            ship_length = len(ship.decks)
            if ship_length == 1:
                single_deck += 1
            elif ship_length == 2:
                double_deck += 1
            elif ship_length == 3:
                triple_deck += 1
            elif ship_length == 4:
                quad_deck += 1
            else:
                raise ValueError("Invalid ship size")
        all_ships = single_deck + double_deck + triple_deck + quad_deck
        if all_ships != 10:
            raise ValueError("Invalid number of ships")
        if (
                single_deck != 4
                or double_deck != 3
                or triple_deck != 2
                or quad_deck != 1
        ):
            raise ValueError("Invalid fleet configuration")

        occupied_cells = {}
        for ship in self.ships:
            for deck in ship.decks:
                cell = (deck.row, deck.column)
                if cell in occupied_cells:
                    raise ValueError("Overlapping ships")
                occupied_cells[cell] = ship

        for (row, col), current_ship in occupied_cells.items():
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    neighbor = (row + dr, col + dc)
                    if neighbor in occupied_cells:
                        neighbor_ship = occupied_cells[neighbor]
                        if neighbor_ship is not current_ship:
                            raise ValueError("Ships are touching")
