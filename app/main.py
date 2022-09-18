class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False

        self.is_drowned = not any(deck.is_alive for deck in self.decks)

        if self.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = {}

        for ship in ships:
            self.field[ship] = Ship(*ship)

        self._validate_field()

    def fire(self, location: tuple):
        for ship in self.field:
            if self.field[ship].get_deck(*location):
                return self.field[ship].fire(*location)

        return "Miss!"

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
                            cell = "□"
                        else:
                            cell = "*"

                line += cell + " "

            print(line)

        print("")

    def _validate_field(self):
        check = len(self.field)
        if check != 10:
            raise Exception("the total number of the ships should be 10")

        check = sum(1 for ship in self.field.values() if len(ship.decks) == 1)
        if check != 4:
            raise Exception("there should be 4 single-deck ships")

        check = sum(1 for ship in self.field.values() if len(ship.decks) == 2)
        if check != 3:
            raise Exception("there should be 3 double-deck ships")

        check = sum(1 for ship in self.field.values() if len(ship.decks) == 3)
        if check != 2:
            raise Exception("there should be 2 three-deck ships")

        check = sum(1 for ship in self.field.values() if len(ship.decks) == 4)
        if check != 1:
            raise Exception("there should be 1 four-deck ship")

        for ship in self.field:
            row1 = ship[0][0] - 1
            row2 = ship[1][0] + 2
            column1 = ship[0][1] - 1
            column2 = ship[1][1] + 2

            for row in range(row1, row2):
                for column in range(column1, column2):
                    for ship2 in self.field:
                        if ship == ship2:
                            continue

                        if self.field[ship2].get_deck(row, column):
                            error = "ships shouldn't be located in the "\
                                    "neighboring cells (even if cells "\
                                    "are neighbors by diagonal)"
                            raise Exception(error, row, column)
