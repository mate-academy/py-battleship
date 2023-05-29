class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        decks = []
        start_row, start_column = self.start
        end_row, end_column = self.end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                decks.append(Deck(start_row, column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                decks.append(Deck(row, start_column))

        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, location: tuple) -> None:
        row, column = location
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            my_ship = Ship(ship[0], ship[1])
            for deck in my_ship.decks:
                self.field[(deck.row, deck.column)] = my_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
