class ShipValidationError(Exception):
    pass


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
        self._create_decks()

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row, column):
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive is True:
                return
        self.is_drowned = True

    def _create_decks(self):
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))
            return
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        if self.start[1] == self.end[1]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.end[1]))


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {}
        self._create_field()
        self._validate_field()

    def fire(self, location: tuple):
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _create_field(self):
        for ship in self.ships:
            ship_obj = Ship(ship[0], ship[1])
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj

    def print_field(self):
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in set(self.field.values()):
            for deck in ship.decks:
                if ship.is_drowned:
                    field[deck.row][deck.column] = "x"
                elif deck.is_alive:
                    field[deck.row][deck.column] = "\u25A1"
                else:
                    field[deck.row][deck.column] = "*"
        for row in field:
            print(*row)

    def _validate_field(self):
        counter = {}
        for ship in set(self.field.values()):
            number_of_decks = len(ship.decks)
            if f"{number_of_decks}-deck ship" in counter:
                counter[f"{number_of_decks}-deck ship"] += 1
            else:
                counter[f"{number_of_decks}-deck ship"] = 1

            if ship.start[0] == ship.end[0]:
                ship_ends = [(ship.start[0], ship.start[1] - 1),
                             (ship.end[0], ship.end[1] + 1)]
                ship_top = [(ship.start[0] - 1, i)
                            for i in range(ship.start[1] - 1,
                                           ship.end[1] + 1)]
                ship_bottom = [(ship.start[0] + 1, i)
                               for i in range(ship.start[1] - 1,
                                              ship.end[1] + 1)]
                coordinates_to_check = ship_ends + ship_top + ship_bottom
                for coordinate in coordinates_to_check:
                    if coordinate in self.field:
                        raise ShipValidationError("Ships shouldn't be located"
                                                  "in the neighboring cells"
                                                  "(even if cells are"
                                                  " neighbors by diagonal)")

            if ship.start[1] == ship.end[1]:
                ship_ends = [(ship.start[0] - 1, ship.start[1]),
                             (ship.end[0] + 1, ship.end[1])]
                left_side = [(i, ship.start[1] - 1)
                             for i in range(ship.start[0] - 1,
                                            ship.end[0] + 1)]
                right_side = [(i, ship.start[1] + 1)
                              for i in range(ship.start[0] - 1,
                                             ship.end[0] + 1)]
                coordinates_to_check = ship_ends + left_side + right_side
                for coordinate in coordinates_to_check:
                    if coordinate in self.field:
                        raise ShipValidationError("Ships shouldn't be located"
                                                  " in the neighboring cells"
                                                  " (even if cells are"
                                                  " neighbors by diagonal)")

        if len(self.ships) == 10:
            if counter["1-deck ship"] != 4:
                raise ShipValidationError("There should be 4"
                                          " single-deck ships")
            if counter["2-deck ship"] != 3:
                raise ShipValidationError("There should be 3"
                                          " double-deck ships")
            if counter["3-deck ship"] != 2:
                raise ShipValidationError("There should be 2"
                                          " three-deck ships")
            if counter["4-deck ship"] != 1:
                raise ShipValidationError("There should be 1"
                                          " four-deck ship")
        else:
            raise ShipValidationError("The total number"
                                      " of the ships should be 10")
