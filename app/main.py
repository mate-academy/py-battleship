class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: Deck,
            end: Deck,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start.row == end.row and start.column == end.column:
            self.decks.append(Deck(start.row, start.column))
        elif start.row == end.row:
            for column_number in range(start.column, end.column + 1):
                self.decks.append(Deck(start.row, column_number))
        elif start.column == end.column:
            for row_number in range(start.row, end.row + 1):
                self.decks.append(Deck(row_number, start.column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError("There is no such deck")

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = not deck.is_alive
        is_decks_alive = []
        for deck in self.decks:
            is_decks_alive.append(deck.is_alive)
        if any(is_decks_alive):
            self.is_drowned = False
        else:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(
                Deck(ship[0][0], ship[0][1]),
                Deck(ship[1][0], ship[1][1])
            )
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def print_field(self) -> list:
        matrix = []
        for row_number in range(0, 10):
            row = []
            for column_number in range(0, 10):
                if (row_number, column_number) in self.field:
                    ship = self.field[(row_number, column_number)]
                    if ship.is_drowned:
                        row.append("x")
                    else:
                        deck = ship.get_deck(row_number, column_number)
                        row.append("o") if deck.is_alive else row.append("*")
                else:
                    row.append("~")
            matrix.append(row)

        for row in matrix:
            print(" ".join(row))
        return matrix

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
