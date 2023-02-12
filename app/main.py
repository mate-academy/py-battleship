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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}  # key ->  coord, value -> class Ship
        for ship in ships:
            ship = Ship(ship[0], ship[1])

            """first option:
        dictionary of field {key -> one cell: value -> one class Ship}"""
            # for deck in ship.decks:
            #     self.field[deck.row, deck.column] = ship

            """second option:
        dictionary of field {key -> tuple of cells: value -> one class Ship}"""
            self.field[
                tuple((deck.row, deck.column) for deck in ship.decks)
            ] = ship

    def fire(self, location: tuple) -> str:
        row, column = location

        """version for first option"""
        # if location in self.field:
        #     self.field[location].fire(row, column)
        #     if self.field[location].is_drowned:
        #         return "Sunk!"
        #     return "Hit!"
        # return "Miss!"

        """version for second option"""
        for ship in self.field:
            if location in ship:
                self.field[ship].fire(row, column)
                if self.field[ship].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
