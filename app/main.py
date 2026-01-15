from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, decks: List[Deck]) -> None:
        self.decks = decks

    def get_deck(self, row: int, col: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == col:
                return deck
        return None

    @property
    def is_drowned(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            decks = []
            if start[0] == end[0]:  # horizontal
                for col in range(start[1], end[1] + 1):
                    decks.append(Deck(start[0], col))
            else:  # vertical
                for row in range(start[0], end[0] + 1):
                    decks.append(Deck(row, start[1]))
            ship = Ship(decks)
            self.ships.append(ship)
            for deck in decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Must be exactly 10 ships")

        lengths = [len(ship.decks) for ship in self.ships]
        expected = {1: 4, 2: 3, 3: 2, 4: 1}
        actual = {length: lengths.count(length) for length in expected}

        if actual != expected:
            raise ValueError(f"Invalid ship distribution: {actual}")

        occupied = set()
        for ship in self.ships:
            for deck in ship.decks:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        neighbor = (deck.row + dr, deck.column + dc)
                        if (neighbor in occupied
                                and neighbor not in [(d.row, d.column)
                                                     for d in ship.decks]):
                            raise ValueError(f"Ships too close at {deck.row}, "
                                             f"{deck.column}")
                occupied.add((deck.row, deck.column))

    def fire(self, target: Tuple[int, int]) -> str:
        ship = self.field.get(target)
        if not ship:
            return "Miss!"

        deck = ship.get_deck(*target)
        if deck and deck.is_alive:
            deck.is_alive = False
            return "Sunk!" if ship.is_drowned else "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        grid: List[List[str]] = [["~" for _ in range(10)] for _ in range(10)]

        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)
            if deck:
                if deck.is_alive:
                    grid[row][col] = "□"
                elif not ship.is_drowned:
                    grid[row][col] = "*"
                else:
                    grid[row][col] = "x"

        for row in grid:
            print(" ".join(row))
