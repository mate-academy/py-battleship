from typing import List, Tuple, Dict, Union


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
        self.decks = [Deck(row, col) for row in range(start[0], end[0] + 1)
                      for col in range(start[1], end[1] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        deck = ship.get_deck(*location)
        if not deck.is_alive:
            return "Already fired here!"
        deck.is_alive = False
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
