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
            # Navio horizontal
            first_column = min(start_col, end_col)
            last_column = max(start_col, end_col)
            for column in range(first_column, last_column + 1):
                decks.append(Deck((start_row, column)))
        elif start_col == end_col:
            # Navio vertical
            first_row = min(start_row, end_row)
            last_row = max(start_row, end_row)
            for row in range(first_row, last_row + 1):
                decks.append(Deck((row, start_col)))
        else:
            raise ValueError("The ship must be horizontal or vertical")
        return decks

    def fire(self, location: tuple[int, int]) -> str:
        for deck in self.decks:
            if deck.position == location:
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

    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.ships = [
            Ship(start_position, end_position)
            for start_position, end_position in ships
        ]
        self.field = self._create_empty_field()
        self._place_ships()

    def _create_empty_field(self) -> None:
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

    def fire(self, location: tuple[int, int]) -> str:
        if not self._is_valid_location(location):
            raise ValueError("Location is outside the field")
        row, col = location
        ship = self.field[row][col]
        if ship is None:
            return "Miss!"
        return ship.fire(location)

    def _is_valid_location(self, location: tuple[int, int],) -> bool:
        if len(location) != 2:
            return False
        row, col = location
        if not isinstance(row, int) or not isinstance(col, int):
            return False
        return (0 <= row < self.FIELD_SIZE and 0 <= col < self.FIELD_SIZE)

    def _get_cell_symbol(self, location: tuple[int, int],
                         ship: Ship | None,) -> str:
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
