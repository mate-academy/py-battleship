from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = None
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.fill_decs()

    def fill_decs(self) -> None:
        self.decks = []

        for coord_x in range(self.start[0], self.end[0] + 1):
            for coord_y in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(coord_x, coord_y))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        if deck is None:
            print(f"No deck found at row {row}, column {column}")
            return

        deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}

        for start, end in self.ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:

        if location in self.field:
            self.field[location].fire(location[0], location[1])

            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
