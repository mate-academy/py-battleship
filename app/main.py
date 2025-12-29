from typing import List, Tuple


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

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
        self,
        start: Tuple[int],
        end: Tuple[int],
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def __repr__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"

    def create_decks(self) -> List[Deck]:
        return [
            Deck(row, column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        return next(
            (
                deck for deck in self.decks
                if deck.row == row and deck.column == column
            ),
            None
        )

    def fire(self, row: int, column: int) -> None:

        attacked_deck = self.get_deck(row, column)
        if attacked_deck:
            attacked_deck.is_alive = False
            self.update_ship_status()

    def update_ship_status(self) -> None:
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int]]]) -> None:

        self.ships = ships
        self.field = {}

        self.ships_position()

    def __repr__(self) -> str:
        return f"{self.field}"

    def ships_position(self) -> None:
        for start, end in self.ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:

        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    if any(deck.is_alive for deck in ship.decks):
                        print(u"\u25A1", end="\t")
                    else:
                        print(u"x", end="\t")
                else:
                    print(u"~", end="\t")
            print("\n")
