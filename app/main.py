class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive:
            bool = True
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
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, col) for row in range(start[0], end[0] + 1)
            for col in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> tuple:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        field_display = ""
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    deck = Deck(self.field[(row, col)].get_deck(row, col))
                    if deck.is_alive:
                        field_display += u"\u25A1 "
                    else:
                        field_display += (
                            "x " if self.field[(row, col)].is_drowned else "* "
                        )
                else:
                    field_display += "~ "
            field_display += "\n"
        print(field_display)
