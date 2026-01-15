from typing import List, Tuple


class Deck:
    def __init__(self, row: int, col: int, alive: bool = True) -> None:
        self.row = row
        self.col = col
        self.alive = alive


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.decks = []
        self.drowned = False
        row_step = start[0] == end[0]
        for i in range(start[row_step], end[row_step] + 1):
            pos = (start[0], i) if row_step else (i, start[1])
            self.decks.append(Deck(*pos))

    def fire(self, row: int, col: int) -> str:
        deck = next(
            (d for d in self.decks
             if d.row == row and d.col == col and d.alive),
            None)
        if deck:
            deck.alive = False
            if all(not d.alive for d in self.decks):
                self.drowned = True
                return "Sunk!"
            return "Hit!"
        return None


class Battleship:
    def __init__(
            self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {
            (d.row, d.col): ship
            for start, end in ships
            for ship in [Ship(start, end)]
            for d in ship.decks
        }

    def fire(self, loc: Tuple[int, int]) -> str:
        ship = self.field.get(loc)
        return ship.fire(*loc) if ship else "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = "".join(self.cell_symbol(row, col) for col in range(10))
            print(line)

    def cell_symbol(self, row: int, col: int) -> str:
        if (row, col) in self.field:
            ship = self.field[(row, col)]
            if ship.decks[0].alive:
                return "□ "
            elif ship.drowned:
                return "x "
            return "* "
        return "~ "
