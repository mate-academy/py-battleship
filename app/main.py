from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks: List[Deck] = []

        r1, c1 = start
        r2, c2 = end
        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int],
                                         Tuple[int, int]]]) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships_list: List[Ship] = []

        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships_list.append(new_ship)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        self._validate_field()

    def _validate_field(self) -> None:
        all_lengths = sorted([len(ship.decks) for ship in self.ships_list])
        expected = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

        if all_lengths != expected:
            raise ValueError("Invalid ship set!")

        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for ship in self.ships_list:
            for deck in ship.decks:
                for dr, dc in offsets:
                    neighbor = (deck.row + dr, deck.column + dc)
                    neighbor_ship = self.field.get(neighbor)
                    if neighbor_ship and neighbor_ship is not ship:
                        raise ValueError(f"Ships too close at {neighbor}!")

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if not ship:
            return "Miss!"

        row, col = location
        ship.fire(row, col)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                ship = self.field.get((row, col))
                symbol = "~"
                if ship:
                    if ship.is_drowned:
                        symbol = "x"
                    else:
                        deck = ship.get_deck(row, col)
                        symbol = "□" if deck and deck.is_alive else "*"
                print(symbol, end=" ")
            print()
