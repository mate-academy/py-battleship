class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        start_row, start_col = start
        end_row, end_col = end
        for row in range(start_row, end_row + 1):
            for column in range(start_col, end_col + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.board = [["0" for _ in range(10)] for _ in range(10)]
        self.missed = []
        self.field = {}
        for ship in ships:
            ship_obj = Ship(*ship)
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(location[0], location[1])
            if not deck.is_alive:
                return "The deck is already hit!"
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        self.missed.append((location[0], location[1]))
        return "Miss!"

    def print_field(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                if not deck.is_alive:
                    self.board[deck.row][deck.column] = "X"
                if deck.is_alive:
                    self.board[deck.row][deck.column] = u"\u25A1"
            for miss in self.missed:
                self.board[miss[0]][miss[1]] = "-"
        for row in self.board:
            print(row)
