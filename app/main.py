class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        self._create_decks(start, end)

    def _create_decks(self, start: tuple, end: tuple) -> None:
        start_row, start_column = start
        end_row, end_column = end
        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self._create_field(ships)

    def _create_field(self, ships: list[tuple]) -> None:
        for ship in ships:
            start, end = ship
            start_row, start_column = start
            end_row, end_column = end
            ship_object = Ship(start, end)
            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    self.field[(row, column)] = ship_object

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
                    deck = ship.get_deck(row, column)

                    if deck.is_alive:
                        print("□", end="\t")
                    if ship.is_drowned:
                        print("x", end="\t")
                    print("*", end="\t")
                print("~", end="\t")
            print()
