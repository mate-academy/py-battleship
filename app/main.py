class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.col = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:

        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.col == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = ships
        for ship in ships:
            start, end = ship
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.col)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line_print = ""
            for col in range(10):
                if self.field.get((row, col)) is None:
                    line_print += " ~ "
                elif self.field.get((row, col)):
                    ship = self.field[(row, col)]
                    if all(not deck.is_alive for deck in ship.decks):
                        line_print += " x "
                    elif any(deck.is_alive is False for deck in ship.decks):
                        if ship.decks[col].is_alive:
                            line_print += u" \u25A1 "
                        else:
                            line_print += " * "
                    else:
                        line_print += u" \u25A1 "
            print(line_print)
