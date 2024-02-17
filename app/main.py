class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(
            self, start: tuple[int, int],
            end: tuple[int, int]) -> None:
        self.decks = []
        self.is_drowned = False
        row_start, col_start = start
        row_end, col_end = end
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            self.is_drowned = all(not deck.is_alive for deck in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self, ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = [Ship(*ship) for ship in ships]
        for ship in self.ships:
            for deck in ship.decks:
                self.field[
                    (deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        row, col = location
        if location in self.field:
            return self.field[location].fire(row, col)
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field \
                        and self.field[(row, col)].get_deck(row, col).is_alive:
                    print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()
