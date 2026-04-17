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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        row1, column1 = start
        row2, column2 = end
        if row1 == row2:
            for column in range(
                    min(column1, column2),
                    max(column1, column2) + 1):
                self.decks.append(Deck(row1, column))

        else:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, column1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            if not deck.is_alive:
                return
            deck.is_alive = False
            if all(not dec.is_alive for dec in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        self.field = {}
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
