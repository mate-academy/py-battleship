class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def str(self) -> None:
        return "□" if self.is_alive else "x"  # "□" for alive, "x" for drowned


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:  # Horizontal ship
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:  # Vertical ship
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True  # Deck is hit
        return False  # No deck at this location


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        # Place ships on the field
        for ship_coords in ships:
            start, end = ship_coords
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> None:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        if ship.fire(location[0], location[1]):
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_display = []
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        row_display.append("□")
                    else:
                        row_display.append("x")
                else:
                    row_display.append("~")
            print(" ".join(row_display))
