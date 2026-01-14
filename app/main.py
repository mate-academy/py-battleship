from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    class Cell:
        class Deck:
            def __init__(
                    self,
                    row: int,
                    column: int,
                    is_alive: bool = True
            ) -> None:
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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.add_deck()

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def add_deck(self) -> List[Deck]:
        decks = []
        if self.start == self.end:
            decks.append(Deck(self.start[0], self.start[1]))
        elif self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.end[1]))
        return decks

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships = ships
        self.field = self.create_ship()

    def create_ship(self) -> Dict[Tuple[int, int], Ship]:
        field = {}
        for ship in self.ships:
            battleship = Ship(ship[0], ship[1])
            for deck in battleship.decks:
                field[(deck.row, deck.column)] = battleship
        return field

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
