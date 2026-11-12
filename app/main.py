from collections import Counter


class Deck:

    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position
        self.is_hit = False


class Ship:

    def __init__(self, start_position: tuple[int, int],
                 end_position: tuple[int, int]) -> None:
        self.start_position = start_position
        self.end_position = end_position
        self.decks = self._create_decks()

    def is_sunk(self) -> bool:
        return all(deck.is_hit for deck in self.decks)

    def _create_decks(self) -> list[Deck]:
        start_row, start_col = self.start_position
        end_row, end_col = self.end_position
        decks = []

        if start_row == end_row:
            # Horizontal ship
            first_column = min(start_col, end_col)
            last_column = max(start_col, end_col)
            for column in range(first_column, last_column + 1):
                decks.append(Deck((start_row, column)))
        elif start_col == end_col:
            # Vertical ship
            first_row = min(start_row, end_row)
            last_row = max(start_row, end_row)
            for row in range(first_row, last_row + 1):
                decks.append(Deck((row, start_col)))
        else:
            raise ValueError("The ship must be horizontal or vertical")
        return decks

    def fire(self, ceil: tuple[int, int]) -> str:
        for deck in self.decks:
            if deck.position == ceil:
                deck.is_hit = True
                if self.is_sunk():
                    return "Sunk!"
                return "Hit!"
        raise ValueError("Location does not belong to the ship")

    def get_deck(self, location: tuple[int, int]) -> Deck | None:
        for deck in self.decks:
            if deck.position == location:
                return deck
        return None


class Battleship:
    FIELD_SIZE = 10
    EMPTY = "~"
    ALIVE_DECK = "□"
    HIT_DECK = "*"
    SUNK_DECK = "x"
    EXPECTED_FLEET = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.ships = [
            Ship(start_position, end_position)
            for start_position, end_position in ships
        ]
        self.field = self._create_empty_field()
        self._place_ships()
        self._validate_field()

    def _create_empty_field(self) -> list[list[Ship | None]]:
        return [
            [None for _ in range(self.FIELD_SIZE)]
            for _ in range(self.FIELD_SIZE)
        ]

    def _place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                row, col = deck.position
                if not self._is_valid_location(deck.position):
                    raise ValueError("Ship is outside the field")
                if self.field[row][col] is not None:
                    raise ValueError("Ships overlap")
                self.field[row][col] = ship

    def _validate_field(self) -> None:
        # 1. Validate total fleet size
        expected_total = sum(self.EXPECTED_FLEET.values())
        if len(self.ships) != expected_total:
            raise ValueError(
                f"Invalid fleet size: "
                f"expected {expected_total}, got {len(self.ships)}"
            )

        # 2. Validate ship lengths distribution
        length_counts = Counter(len(ship.decks) for ship in self.ships)
        if dict(length_counts) != self.EXPECTED_FLEET:
            raise ValueError(
                f"Invalid ship lengths distribution: "
                f"expected {self.EXPECTED_FLEET}, got {dict(length_counts)}"
            )

        # 3. Validate that ships do not touch (including diagonally)
        for ship in self.ships:
            for deck in ship.decks:
                row, col = deck.position
                for d_row in (-1, 0, 1):
                    for d_col in (-1, 0, 1):
                        if d_row == 0 and d_col == 0:
                            continue
                        n_row, n_col = row + d_row, col + d_col
                        if (0 <= n_row < self.FIELD_SIZE
                                and 0 <= n_col < self.FIELD_SIZE):
                            neighbor_ship = self.field[n_row][n_col]
                            if (neighbor_ship is not None
                                    and neighbor_ship is not ship):
                                raise ValueError(
                                    "Ships cannot touch "
                                    "each other, including diagonally")

    def fire(self, ceil: tuple[int, int]) -> str:
        if not self._is_valid_location(ceil):
            raise ValueError("Location is outside the field")
        row, col = ceil
        ship = self.field[row][col]
        if ship is None:
            return "Miss!"
        return ship.fire(ceil)

    def _is_valid_location(self, location: tuple[int, int]) -> bool:
        if len(location) != 2:
            return False
        row, col = location
        if not isinstance(row, int) or not isinstance(col, int):
            return False
        return 0 <= row < self.FIELD_SIZE and 0 <= col < self.FIELD_SIZE

    def _get_cell_symbol(self, location: tuple[int, int],
                         ship: Ship | None) -> str:
        if ship is None:
            return self.EMPTY
        deck = ship.get_deck(location)
        if deck is None:
            return self.EMPTY
        if not deck.is_hit:
            return self.ALIVE_DECK
        if ship.is_sunk():
            return self.SUNK_DECK
        return self.HIT_DECK

    def print_field(self) -> None:
        for row in range(self.FIELD_SIZE):
            symbols = []
            for col in range(self.FIELD_SIZE):
                ship = self.field[row][col]
                symbol = self._get_cell_symbol((row, col), ship)
                symbols.append(symbol)
            print("\t".join(symbols))
