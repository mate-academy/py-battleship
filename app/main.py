from dataclasses import dataclass
from app.validation import validate_field


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = None
        self.create_decks()

    def create_decks(self) -> None:

        if self.start[0] == self.end[0]:
            decks_number = abs(self.end[1] - self.start[1])
            initial_cell = min(self.end[1], self.start[1])
            self.decks = [
                Deck(self.start[0], deck)
                for deck in range(initial_cell,
                                  initial_cell + 1 + decks_number)
            ]
        elif self.start[1] == self.end[1]:
            decks_number = abs(self.end[0] - self.start[0])
            initial_cell = min(self.end[0], self.start[0])
            self.decks = [
                Deck(deck, self.start[1])
                for deck in range(initial_cell,
                                  initial_cell + 1 + decks_number)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.column == column and deck.row == row:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = not any(list(deck.is_alive for deck in self.decks))


class Battleship:
    def __init__(self, ships: list) -> None:
        ships = validate_field(ships)
        if not ships:
            raise ValueError("Enter correct ships list")
        self.field = {}
        ship_list = [Ship(ship[0], ship[1]) for ship in ships]
        for ship in ship_list:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
