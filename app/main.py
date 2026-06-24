from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.decks: List[Deck] = []
        self._create_decks()

    def _create_decks(self) -> None:
        ro1, col1 = self.start
        ro2, col2 = self.end
        if ro1 == ro2:
            for col in range(col1, col2 + 1):
                deck = Deck(ro1, col, True)
                deck.ship = self
                self.decks.append(deck)
        elif col1 == col2:
            for ro in range(ro1, ro2 + 1):
                deck = Deck(ro, col1, True)
                deck.ship = self
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship_data in ships:
            ship = Ship(ship_data[0], ship_data[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = deck

    def fire(self, ceil: tuple[int, int]) -> str:
        row, column = ceil
        deck = self.field.get((row, column))
        if not deck:
            return "Miss!"
        deck.is_alive = False
        ship = deck.ship
        alive_decks = sum(1 for d in ship.decks if d.is_alive)
        if alive_decks == 0:
            return "Sunk!"
        return "Hit!"
