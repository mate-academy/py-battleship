from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks: List[Deck] = []
        self.is_drowned = is_drowned

        r1, c1 = start
        r2, c2 = end

        if start == end:
            self.decks.append(Deck(r1, c1))
        elif r1 != r2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))
        elif c1 != c2:
            for column in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        for start, end in ships:
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(*location)

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif deck and not deck.is_alive:
                        print("*", end=" ")
                    else:
                        print("\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> bool:
        unique_ships = list(set(self.field.values()))
        if len(unique_ships) != 10:
            return False

        lengths = [len(ship.decks) for ship in unique_ships]
        for size in range(1, 5):
            if lengths.count(size) != (5 - size):
                return False

        for ship in unique_ships:
            for deck in ship.decks:
                for r_offset in range(deck.row - 1, deck.row + 2):
                    for c_offset in range(deck.column - 1, deck.column + 2):
                        neighbor = (r_offset, c_offset)
                        if (neighbor != (deck.row, deck.column)
                                and neighbor in self.field
                                and self.field[neighbor] is not ship):
                            raise ValueError("Ships cannot be adjacent to each other.")
        return True
