class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.decks = self.make_decks_for_ship()
        self.is_drowned = is_drowned

    def make_decks_for_ship(self):
        decks = []
        ship_length = self.end[0] - self.start[0] + self.end[1] - self.start[1]
        for i in range(0, ship_length + 1):
            if self.start[0] == self.end[0]:
                decks.append(Deck(self.start[0], self.start[1] + i))
            else:
                decks.append(Deck(self.start[0] + i, self.start[1]))
        return decks

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        self.is_drowned = True
        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = self.making_ships()

    def making_ships(self):
        field = {}
        for ship in self.ships:
            ship1 = Ship(ship[0], ship[1])
            for point in ship1.decks:
                field[(point.row, point.column)] = ship1
        return field

    def fire(self, location: tuple):
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
