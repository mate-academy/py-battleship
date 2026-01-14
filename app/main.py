class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self):
        if self.is_alive:
            return u"\u25A1"
        return "*"


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = self._get_ship_decks(start, end)
        self.is_drowned = is_drowned

    def _get_ship_decks(self, start: tuple, end: tuple):
        start_row, start_column = start
        end_row, end_column = end
        decks = []

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                decks.append(Deck(start_row, column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                decks.append(Deck(row, end_column))

        return decks

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck in self.decks:
            deck.is_alive = False

        decks_status = any([deck.is_alive for deck in self.decks])
        if not decks_status:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = self._get_decks_coordinates(ships)
        self._validate_field()

    def _get_decks_coordinates(self, ships):
        decks_cells = dict()
        for ship in ships:
            decks = Ship(*ship)

            for deck in decks.decks:
                decks_cells[(deck.row, deck.column)] = decks

        return decks_cells

    def fire(self, location: tuple):
        if location in self.field:
            self.field[location].fire(*location)

            if self.field[location].is_drowned:
                return "Sunk!"

            return "Hit!"
        return "Miss!"

    def print_field(self):
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        print("x", end="\t")

                    if not ship.is_drowned:
                        print(ship.get_deck(row, column), end="\t")

                else:
                    print("~", end="\t")
            print("")

    def _validate_field(self):
        ships_on_field = set(self.field.values())
        if len(ships_on_field) != 10:
            raise Exception("The total number of the ships should be 10")

        amount_ship_decks = []
        for ship in ships_on_field:
            amount_ship_decks.append(len(ship.decks))
        if amount_ship_decks.count(1) != 4:
            raise Exception("The total number of the single-deck "
                            "ships should be 4")
        if amount_ship_decks.count(2) != 3:
            raise Exception("The total number of the double-deck "
                            "ships should be 3")
        if amount_ship_decks.count(3) != 2:
            raise Exception("The total number of the three-deck "
                            "ships should be 2")
        if amount_ship_decks.count(4) != 1:
            raise Exception("The total number of the four-deck "
                            "ships should be 1")

        for deck, ship in self.field.items():
            test_suite = (-1, 0), (1, 0), (0, -1), (0, 1), \
                         (-1, 1), (1, -1), (-1, -1), (1, 1)
            for row_limit, column_limit in test_suite:
                test_case = (deck[0] + row_limit, deck[1] + column_limit)

                if test_case in self.field.keys() \
                        and ship is not self.field[test_case]:
                    raise Exception("Ships shouldn't be located "
                                    "in the neighboring cells")
