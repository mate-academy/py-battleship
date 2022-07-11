class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        ship_length = end[0] - start[0] + end[1] - start[1]
        for i in range(0, ship_length + 1):
            if start[0] == end[0]:
                self.decks.append(Deck(start[0], start[1] + i))
            else:
                self.decks.append(Deck(start[0] + i, start[1]))
        self.is_drowned = is_drowned

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
        self.field = {}
        for ship in ships:
            ship1 = Ship(ship[0], ship[1])
            for point in ship1.decks:
                self.field[(point.row, point.column)] = ship1

    def fire(self, location: tuple):
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
