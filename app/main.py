class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        start_row, start_col = self.start
        end_row, end_col = self.end

        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                deck = Deck(start_row, col)
                self.decks.append(deck)
        elif start_col == end_col:
            for row in range(start_row, end_row + 1):
                deck = Deck(row, start_col)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple[int, int], tuple[int, int]]) -> None:
        self.field = {}
        self.ships = [Ship(*ship) for ship in ships]
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field_size = 10
        for row in range(field_size):
            for col in range(field_size):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        print("□", end="\t")
                    else:
                        print("x", end="\t")
                else:
                    print("~", end="\t")
            print()
