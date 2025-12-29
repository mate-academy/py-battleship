from collections import Counter


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.is_alive = is_alive
        self.column = column
        self.row = row


class Ship:
    def __init__(
            self, start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []
        _coordinates: list[tuple[int, int]] = []
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row=row, column=col))
                _coordinates.append((row, col))
        self.coordinates = tuple(_coordinates)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field: dict[tuple[tuple[int, int], ...], Ship] = {}
        self.fired_locations: set[tuple[int, int]] = set()
        for start, end in ships:
            ship = Ship(start=start, end=end)
            self.field[ship.coordinates] = ship

    def fire(self, location: tuple[int, int]) -> str:
        self.print_field()

        if location in self.fired_locations:
            return "Already fired!"

        self.fired_locations.add(location)

        for coordinates, ship in self.field.items():
            if location in coordinates:
                ship.fire(*location)
                return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        ship_lengths = Counter(len(ship.decks) for ship in self.field.values())

        expected_lengths = {1: 4, 2: 3, 3: 2, 4: 1}

        if len(self.field) != 10 or ship_lengths != expected_lengths:
            raise ValueError("Invalid number or types of ships")

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                symbol = self.get_symbol(location)
                print(symbol, end=" ")
            print()

    def get_symbol(self, location: tuple[int, int]) -> str:
        for coordinates, ship in self.field.items():
            if location in coordinates:
                deck = ship.get_deck(*location)
                if deck and not deck.is_alive:
                    return "x" if ship.is_drowned else "*"
                else:
                    return u"\u25A1"
        return "~"
