class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        if self.start[0] == self.end[0]:  # horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:  # vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not one_deck.is_alive for one_deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field_display = [["~" for _ in range(10)] for _ in range(10)]
        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)
            if deck.is_alive:
                field_display[row][col] = "□"
            else:
                if ship.is_drowned:
                    field_display[row][col] = "x"
                else:
                    field_display[row][col] = "*"
        for row in field_display:
            print(" ".join(row))
