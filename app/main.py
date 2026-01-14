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
        self.creat_ships()

    def creat_ships(self):
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))

        elif self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

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
        self.field = {}
        self._create_field()

    def fire(self, location: tuple):
        if location not in self.field:
            return "Miss!"

        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def _create_field(self):
        for ship in self.ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def print_field(self):
        for row in range(10):
            line = ""
            for column in range(10):
                cell = "~"
                for ship in self.field:
                    deck = self.field[ship].get_deck(row, column)
                    if deck:
                        if self.field[ship].is_drowned:
                            cell = "x"
                        elif deck.is_alive:
                            cell = u"\u25A1"
                        else:
                            cell = "*"
                line += cell + " "
            print(line)
        print("")

    def _validate_field(self):
        numbers_ship = [len(ship) for ship in self.field.keys()]

        if len(numbers_ship) != 10:
            raise Exception("The total number of the ships should be 10")

        if numbers_ship.count(4) != 1:
            raise Exception("There should be four single-deck ships")

        if numbers_ship.count(3) != 2:
            raise Exception("There should be three double-deck ships")

        if numbers_ship.count(2) != 3:
            raise Exception("There should be two three-deck ships")

        if numbers_ship.count(1) != 4:
            raise Exception("There should be one four-deck ship")
