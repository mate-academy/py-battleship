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
        list_start = list(self.start)
        list_end = list(self.end)

        if list_start == list_end:
            self.decks.append(Deck(list_start[0], list_start[1]))

        if list_start[0] != list_end[0]:
            for points in range(list_start[0], list_end[0] + 1):
                self.decks.append(Deck(points, list_start[1]))

        if list_start[1] != list_end[1]:
            for points in range(list_start[1], list_end[1] + 1):
                self.decks.append(Deck(list_start[0], points))

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
        self.field = Battleship.create(self)

    def create(self):
        list_ships = []
        for ships in self.ships:
            battle_ships = list(ships)
            list_ships.append(Ship(battle_ships[0], battle_ships[1]))
        for create_decks in list_ships:
            create_decks.decks_create()
        for crate_field in list_ships:
            for j in range(len(crate_field.decks) - 1):
                self.field.update({(crate_field.decks[j].row,
                                    crate_field.decks[j].column): crate_field})
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
