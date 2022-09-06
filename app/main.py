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
        self.decks_in_list = []
        self.decks_list()

    def decks_list(self):
        if self.start[0] == self.end[0] and self.start[1] != self.end[1]:
            for column_ in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column_))
        if self.start[1] == self.end[1] and self.start[0] != self.end[0]:
            for row_ in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row_, self.end[1]))
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.end[1]))
        return self.decks

    def get_deck(self, row, column):
        for object_d in self.decks:
            if object_d.row == row and object_d.column == column:
                return object_d

    def fire(self, row, column):
        obj_deck = self.get_deck(row, column)
        obj_deck.is_alive = False
        self.decks_in_list.append(obj_deck)
        if len(self.decks_in_list) == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {}
        self.battle_ship = None
        self.field_battle()

    def field_battle(self):
        for ship in self.ships:
            ship_obj = Ship(ship[0], ship[1])
            if ship[0][0] == ship[1][0] and ship[0][1] != ship[1][1]:
                for column_ in range(ship[0][1], ship[1][1] + 1):
                    self.field[(ship[0][0], column_)] = ship_obj
            if ship[0][1] == ship[1][1] and ship[0][0] != ship[1][0]:
                for row_ in range(ship[0][0], ship[1][0] + 1):
                    self.field[(row_, ship[0][1])] = ship_obj
            if ship[0][0] == ship[1][0] and ship[0][1] == ship[1][1]:
                self.field[(ship[0][0], ship[0][1])] = ship_obj
        return self.field

    def fire(self, location: tuple):
        self.print_field()
        if (location[0], location[1]) not in self.field:
            return "Miss!"
        ship_object = self.field[location]
        ship_object.fire(location[0], location[1])
        print(ship_object.is_drowned)
        if (location[0], location[1]) in self.field and ship_object.is_drowned:
            self.print_field()
            print('\n'.join('\t'.join(map(str, row))
                            for row in self.battle_ship))
            return "Sunk!"
        if (location[0], location[1]) in self.field and \
                self.battle_ship[location[0]][location[1]] == u"\u25A1":
            self.print_field()
            print('\n'.join('\t'.join(map(str, row))
                            for row in self.battle_ship))
            return "Hit!"

    def print_field(self):
        battle_ = [['~'] * 10 for i in range(10)]
        decks_on_field = []
        for key in self.field:
            decks_on_field.append(key)
        for row, column in decks_on_field:
            ship = self.field[(row, column)]
            if ship.get_deck(row, column).is_alive:
                battle_[row][column] = u"\u25A1"
            if ship.is_drowned:
                decks_ = ship.decks_list()
                for deck_ in decks_:
                    battle_[deck_.row][deck_.column] = "x"
            elif not ship.get_deck(row, column).is_alive:
                battle_[row][column] = "*"
        self.battle_ship = battle_
        return self.battle_ship
