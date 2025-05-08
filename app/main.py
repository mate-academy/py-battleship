class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start[0] != self.end[0]:
            row = self.start[0]
            col = self.start[1]
            self.decks.append(Deck(row, col))
            while row != self.end[0]:
                row += 1
                self.decks.append(Deck(row, col))

        else:
            row = self.start[0]
            col = self.start[1]
            self.decks.append(Deck(row, col))
            while col != self.end[1]:
                col += 1
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        self.obj_ships = []
        for ship in self.ships:
            start, end = ship
            obj_ship = Ship(start, end)
            self.obj_ships.append(obj_ship)
            for deck in obj_ship.decks:
                self.field[(deck.row, deck.column)] = obj_ship

    def fire(self, location: tuple) -> None:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(location[0], location[1])
            deck.is_alive = False

            if not any([deck.is_alive for deck in ship.decks]):
                ship.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
