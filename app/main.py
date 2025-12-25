from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks: List[Deck] = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = [Ship(start, end) for start, end in ships]
        self._create_field()
        self._validate_field()

    def _create_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        # Count ships by length
        ship_lengths = [len(ship.decks) for ship in self.ships]
        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}

        # Check for required counts of ship types
        for length, required_count in expected_counts.items():
            if ship_lengths.count(length) != required_count:
                raise ValueError(f"Incorrect number of {length}-deck ships.")

        # Check for ships in neighboring cells
        for (row, col), ship in self.field.items():
            for dr in range(-1, 2):  # Neighbor offsets including diagonals
                for dc in range(-1, 2):
                    if (dr, dc) == (0, 0):
                        continue
                    neighbor = (row + dr, col + dc)
                    if neighbor in self.field and self.field[neighbor] is not ship:
                        raise ValueError(
                            "Ships are placed in neighboring cells."
                        )

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            row, column = location
            return ship.fire(row, column)
        else:
            return "Miss!"

    def print_field(self) -> None:
        field_representation = [["~"] * 10 for _ in range(10)]
        for (row, col), ship in self.field.items():
            symbol = "□" if ship.get_deck(row, col).is_alive else "*"
            field_representation[row][col] = symbol
            if ship.is_drowned:
                field_representation[row][col] = "x"

        for row in field_representation:
            print(" ".join(row))
