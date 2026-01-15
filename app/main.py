from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.hit()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
                 ) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        grid = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    grid[deck.row][deck.column] = "□"
                else:
                    grid[deck.row][deck.column] = (
                        "x" if ship.is_drowned else "*"
                    )

        for row in grid:
            print(" ".join(row))
