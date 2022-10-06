class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def decks_create(self):

        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))

        if self.start[0] != self.end[0]:
            for points in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(points, self.start[1]))

        if self.start[1] != self.end[1]:
            for points in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], points))

        self.decks.append(self.is_drowned)
        return self.decks

    def get_deck(self, row, column):
        for deck in range(0, len(self.decks) - 1):
            if self.decks[deck].row == row and \
                    self.decks[deck].column == column:
                return Deck(row, column)

    def fire(self, row, column):
        for deck in range(0, len(self.decks) - 1):
            if self.decks[deck].row == row and \
                    self.decks[deck].column == column:
                self.decks[deck].is_alive = False
        list = []
        for decks in range(0, len(self.decks) - 1):
            list.append(self.decks[decks].is_alive)
        if sum(list) == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships, field={}):
        self.ships = ships
        self.field = field
        self.field = Battleship.create_field(self)

    def create_field(self):
        list_ships = []
        for ships in self.ships:
            list_ships.append(Ship(ships[0], ships[1]))
        for ship in list_ships:
            ship.decks_create()
        for ship in list_ships:
            for j in range(len(ship.decks) - 1):
                self.field.update({(ship.decks[j].row,
                                    ship.decks[j].column): ship})
        return self.field

    def fire(self, location: tuple):

        if location not in self.field.keys():
            return "Miss!"
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned is False:
                return "Hit!"
            elif self.field[location].is_drowned is True:
                return "Sunk!"
