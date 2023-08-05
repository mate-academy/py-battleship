class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        start_row, start_col = start
        end_row, end_col = end
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        self.field = {}
        self._create_field(ships)

    def _create_field(self, ships: list[tuple]) -> None:
        for ship in ships:
            start, end = ship
            start_row, start_col = start
            end_row, end_col = end
            ship_object = Ship(start, end)
            for row in range(start_row, end_row + 1):
                for col in range(start_col, end_col + 1):
                    self.field[(row, col)] = ship_object

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)

                    if deck.is_alive:
                        print((u"\u25A1"), end="\t")
                    if ship.is_drowned:
                        print("x", end="\t")
                    print("*", end="\t")
                print("~", end="\t")
            print()
