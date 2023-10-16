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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        row_start, columns_start = start
        row_end, column_end = end
        for row in range(row_start, row_end + 1):
            for column in range(columns_start, column_end + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.field = {}
        for item in ships:
            start, end = item
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field.update(
                    {(deck.row, deck.column): ship}
                )

    def fire(self, coordinates: tuple) -> str:
        if coordinates not in self.field:
            return "Miss!"
        ship = self.field[coordinates]
        start, end = coordinates
        ship.fire(start, end)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["🌊"] * 10 for _ in range(10)]
        for row in range(10):
            for column in range(10):
                coordinates = (row, column)
                if coordinates in self.field:
                    current_ship = self.field[coordinates]
                    deck = current_ship.get_deck(row, column)
                    if deck.is_alive:
                        field[row][column] = "🚢"
                    elif not deck.is_alive and not current_ship.is_drowned:
                        field[row][column] = "🔥"
                    elif not deck.is_alive and current_ship.is_drowned:
                        field[row][column] = "❌"

        for row in field:
            print("     ".join(row))
