from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.add_decks_to_ship()

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True

    def add_decks_to_ship(self) -> List[Deck]:
        decks = []
        if self.start == self.end:
            decks.append(Deck(self.start[0], self.start[1]))
        elif self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], i))
        else:
            for i in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(i, self.start[1]))
        return decks


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = ships
        self.field = self.not_empty_cells()

    def not_empty_cells(self) -> dict:
        field = {}
        for elem in self.ships:
            ship = Ship(elem[0], elem[1])
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
