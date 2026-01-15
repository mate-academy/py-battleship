class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        return None

    def fire(self, row, column):
        drowned = True
        deck_fire = self.get_deck(row, column)
        deck_fire.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                drowned = False
        if drowned:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship_loc in ships:
            ship = Ship(ship_loc[0], ship_loc[1])
            for row in range(ship_loc[0][0], ship_loc[1][0] + 1):
                for column in range(ship_loc[0][1], ship_loc[1][1] + 1):
                    self.field[(row, column)] = ship

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        else:
            return "Miss!"

    def print_field(self):
        field_print = ""
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        field_print += u"\u25A1  "
                    elif not deck.is_alive and not ship.is_drowned:
                        field_print += "*  "
                    else:
                        field_print += "X  "
                else:
                    field_print += "~  "
            field_print += "\n"
        print(field_print)
