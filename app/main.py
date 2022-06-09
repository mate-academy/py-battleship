class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.deck = (self.row, self.column)
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):

        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks.append(Deck(*start))

        elif start[0] == end[0]:
            for x in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], x))

        elif start[1] == end[1]:
            for x in range(start[0], end[0] + 1):
                self.decks.append(Deck(x, start[1]))

    def get_deck(self, row, column):

        for num, deck in enumerate(self.decks):
            if deck.row == row and deck.column == column:
                return self.decks[num]

    def fire(self, row, column):

        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False

        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple):

        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_deck(self):

        for x in range(10):
            line = []
            for y in range(10):
                if (x, y) not in self.field:
                    line.append(" ~ ")
                else:
                    if self.field[(x, y)].is_drowned:
                        line.append(" X ")
                        continue
                    for deck in self.field[(x, y)].decks:
                        if deck.row == x and deck.column == y:
                            if deck.is_alive:
                                line.append(" □ ")
                            else:
                                line.append(" * ")
            print(*line)

    def _validate_field(self):

        validator = {1: 4, 2: 6, 3: 6, 4: 4}
        field_check = {1: 0, 2: 0, 3: 0, 4: 0}

        for deck in self.field:

            field_check[len(self.field[deck].decks)] += 1
            row = deck[0]
            column = deck[1]

            for x in range(row - 1, row + 2):
                for y in range(column - 1, column + 2):
                    if (x, y) in self.field:
                        if (x, y) not in [decks.deck
                                          for decks
                                          in self.field[deck].decks]:
                            raise ValueError("there are ships "
                                             "shouldn't be located in"
                                             " the neighboring cells")

        if not validator == field_check:
            raise KeyError("you should write a right count of ships: "
                           "1deck_ship = 4, 2deck_ship = 3,"
                           " 3deck_ship = 2, 4deck_ship = 1")
