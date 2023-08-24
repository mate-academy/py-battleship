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
        if start[0] == end[0] and start[1] != end[1]:
            index = 0
            for _ in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0],
                                       start[1] + index,
                                       is_alive=True))
                index += 1
        elif start[1] == end[1] and start[0] != end[0]:
            index = 0
            for _ in range(start[0], end[0] + 1):
                self.decks.append(Deck(start[0] + index,
                                       start[1],
                                       is_alive=True))
                index += 1
        else:
            self.decks.append(Deck(start[0], start[1], is_alive=True))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        check = []
        for deck in self.decks:
            if not deck.is_alive:
                check.append(True)
            else:
                check.append(False)
        if all(check):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = []
        for ship in ships:
            self.ships.append(Ship(ship[0], ship[1], is_drowned=False))

        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
