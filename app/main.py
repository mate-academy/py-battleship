class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        start_row, start_column = start
        end_row, end_column = end
        if start_column == end_column:
            min_value, max_value = start_row, end_row
        else:
            min_value, max_value = start_column, end_column
        while min_value <= max_value:
            if start_column == end_column:
                self.decks.append(Deck(min_value, start_column))
            else:
                self.decks.append(Deck(start_row, min_value))
            min_value += 1

    def get_deck(self, row, column) -> Deck:
        return self.decks[self.decks.index(Deck(row, column))]

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive is True:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        self.around_points = []
        field = self.field
        self.ships = []
        self.miss_shots = {}
        for ship in ships:
            field_ship = Ship(ship[0], ship[1])
            for deck in field_ship.decks:
                field[(deck.row, deck.column)] = field_ship
            self.ships.append(field_ship)
        self._validate_field()

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        self.miss_shots[location] = "*"
        return "Miss!"

    def print_field(self):
        for row in range(10):
            print_str = ""
            for column in range(10):
                status = "~"
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        status = "x"
                    elif not ship.get_deck(row, column).is_alive:
                        status = "*"
                    else:
                        status = "□"
                elif (row, column) in self.miss_shots:
                    status = "."
                print_str += status + " "
            print(print_str)

    def _validate_field(self):
        if not len(self.ships) == 10:
            raise Exception("The total number of the ships should be 10")
        check_count_by_types = {4: 1, 3: 2, 2: 3, 1: 4}
        count_by_types = {4: 0, 3: 0, 2: 0, 1: 0}
        self.around_points = []
        for ship in self.ships:
            min_r = ship.decks[0].row
            min_c = ship.decks[0].column
            max_r = ship.decks[len(ship.decks) - 1].row
            max_c = ship.decks[len(ship.decks) - 1].column
            if min_c == max_c:
                a, b = min_r - 1, max_r + 1
                self.around_points.append((a, min_c))
                while a <= b:
                    self.around_points.append((a, min_c - 1))
                    self.around_points.append((a, min_c + 1))
                    a += 1
                self.around_points.append((b, min_c))
            else:
                a, b = min_c - 1, max_c + 1
                self.around_points.append((min_r, a))
                while a <= b:
                    self.around_points.append((min_r - 1, a))
                    self.around_points.append((min_r + 1, a))
                    a += 1
                self.around_points.append((min_r, b))
            count_by_types[len(ship.decks)] += 1
        if not check_count_by_types == count_by_types:
            raise Exception("- there should be 4 single-deck ships "
                            "- there should be 3 double-deck ships "
                            "- there should be 2 three-deck ships "
                            "- there should be 1 four-deck ship")
        for ship in self.ships:
            for deck in ship.decks:
                if (deck.row, deck.column) in self.around_points:
                    raise Exception(
                        "ships shouldn't be located "
                        "in the neighboring cells "
                        "(even if cells are neighbors by diagonal)")
