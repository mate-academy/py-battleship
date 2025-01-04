from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.decks: List[Deck] = self._create_decks(start, end)
        self.is_drowned: bool = False

    def _create_decks(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> List[Deck]:
        decks: List[Deck] = []
        if start[0] == end[0]:  # Horizontal ship
            for col in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], col))
        elif start[1] == end[1]:  # Vertical ship
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
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
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = [Ship(start, end) for start, end in ships]
        self.field: Dict[Tuple[int, int], Ship] = {}
        self._initialize_field()
        self._validate_field()

    def _initialize_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        hit = ship.fire(*location)
        if hit:
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field: List[List[str]] = [["~" for _ in range(10)] for _ in range(10)]
        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)
            if deck.is_alive:
                field[row][col] = "□"  # Alive deck
            elif ship.is_drowned:
                field[row][col] = "x"  # Drowned deck
            else:
                field[row][col] = "*"  # Hit deck of alive ship

        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        ship_lengths: List[int] = [len(ship.decks) for ship in self.ships]
        if len(ship_lengths) != 10:
            raise ValueError("There must be exactly 10 ships.")

        counts: Dict[int, int] = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        for length in ship_lengths:
            if length > 4:
                raise ValueError("Ship lengths cannot exceed 4.")
            counts[length] += 1

        if (counts[1] != 4 or counts[2] != 3
                or counts[3] != 2 or counts[4] != 1):
            raise ValueError("Invalid ship configuration.")

        for ship in self.ships:
            for deck in ship.decks:
                for row in range(deck.row - 1, deck.row + 2):
                    for col in range(deck.column - 1, deck.column + 2):
                        if ((row, col) in self.field
                                and self.field[(row, col)] != ship):
                            raise ValueError("Ships cannot be adjacent.")
