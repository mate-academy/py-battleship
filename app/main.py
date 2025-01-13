from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int],
                 end: Tuple[int, int], is_drowned: bool = False) -> None:
        self.decks = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self,
                 ships: List[
                     Tuple[Tuple[int, int], Tuple[int, int]]
                 ]) -> None:
        self.field = [
            [None for _ in range(10)] for _ in range(10)
        ]
        self.ships: List[Ship] = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[deck.row][deck.column] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        ship = self.field[row][col]
        if ship is None:
            return "Miss!"
        return ship.fire(row, col)
