from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks: List[Deck] = []
        self.is_drowned = is_drowned
        self.create_decks(start, end)

    def create_decks(self, start: Tuple[int, int],
                     end: Tuple[int, int]) -> None:
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                self.decks.append(Deck(start_row, col))
        elif start_col == end_col:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, start_col))

    def get_deck(self, row: int, column: int) -> Deck:
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
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]])\
            -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        if (row, col) in self.field:
            ship = self.field[(row, col)]
            if ship.fire(row, col):
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
            return "Hit!"
        return "Miss!"
