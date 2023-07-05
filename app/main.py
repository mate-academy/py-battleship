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
        self.start = Deck(start[0], start[1])
        self.end = Deck(end[0], end[1])
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        diff_row = self.end.row - self.start.row
        diff_column = self.end.column - self.start.column
        return [
            Deck(self.start.row + i, self.start.column)
            if diff_row != 0
            else Deck(self.start.row, self.start.column + j)
            for j in range(diff_column + 1)
            for i in range(diff_row + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if sum([deck.is_alive for deck in self.decks]) == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int]]]) -> None:
        self.ships = ships
        self.field = {}
        self.create_field()

    def create_field(self) -> None:
        instances_of_ships = []
        for ship in self.ships:
            instances_of_ships.append(Ship(ship[0], ship[1]))
        for ship_instance in instances_of_ships:
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
