class Deck:

    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.decks = []
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        else:
            for j in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(j, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        try:
            deck.is_alive = False
            if any([j.is_alive for j in self.decks]) is True:
                return self.decks
            self.is_drowned = True
            return self.is_drowned
        except AttributeError:
            return


class Battleship:
    def __init__(self, ships):
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self.empty_field = [["~" for _ in range(10)] for _ in range(10)]
        # is_field_empty was created because realization was made
        # using print_field method which is called in fire method.
        self.is_field_empty = None
        self.drowned_decks = []
        # Created to check the amount of ships and their decks
        self.total_ships = {4: 0, 3: 0, 2: 0, 1: 0}

    def fire(self, location: tuple):
        if self.is_field_empty is None:
            self.print_field()
            self.is_field_empty = "Not Empty"
        x, y = location[0], location[1]
        if self.empty_field[x][y] == "\u25A1":
            self.empty_field[x][y] = "*"
            self.drowned_decks.append([x, y])
            for key, value in self.field.items():
                if value.is_drowned is False:
                    result = Ship.fire(value, x, y)
                    if result is True:
                        value.is_drowned = True
                        self.ship_is_drowned()
                        return "Sunk!"
            return "Hit!"
        return "Miss!"

    def ship_is_drowned(self):
        for deck in self.drowned_decks:
            row, column = deck[0], deck[1]
            self.empty_field[row][column] = "x"
        self.drowned_decks = []

    def print_field(self):
        ship_symbol = "\u25A1"
        for ships in self.field.keys():
            current_ship = Ship(list(ships[0]), list(ships[1]))
            self.field[ships] = current_ship
            # Checking ship way
            row = ships[1][0] - ships[0][0]
            column = ships[1][1] - ships[0][1]
            # Checking ship length
            self.set_ships(max(row, column))
            # Getting indexes which we will use to set ships
            r = ships[0][0]
            c = ships[0][1]
            if row != 0:
                for r_index in range(row + 1):
                    self.empty_field[r][c] = ship_symbol
                    r += 1
                continue
            for c_index in range(column + 1):
                self.empty_field[r][c] = ship_symbol
                c += 1

    def set_ships(self, ship_length: int):
        self.total_ships[ship_length + 1] += 1
        return

    def checking_ship_distance(self):
        for ships in self.field.values():
            if ships.start[0] == ships.end[0]:
                row = ships.start[0]
                start = ships.start[1] - 1 if ships.start[1] - 1 >= 0 else 0
                end = ships.end[1] + 1 if ships.end[1] + 1 <= 9 else 9
                # Checking cell from the left side of the ship
                if start != ships.start[1] and \
                        self.empty_field[row][start] == "\u25A1":
                    return "Ships are too close"
                # Checking cell from the right side of the ship
                if end != ships.end[1] and \
                        self.empty_field[row][end] == "\u25A1":
                    return "Ships are too close"
                # Checking cells in rows under and above the ship
                for c in range(start, ships.end[1] + 2):
                    try:
                        if self.empty_field[row + 1][c] == "\u25A1" \
                                or self.empty_field[row - 1][c] == "\u25A1":
                            return "Ships are too close"
                    except IndexError:
                        continue
            # Checking cells in columns from left and right side of the ship
            else:
                column = ships.start[1]
                start = ships.start[0] - 1 if ships.start[0] - 1 >= 0 else 0
                end = ships.end[0] + 1 if ships.end[0] + 1 <= 9 else 9
                # Checking cell above the ship
                if start != ships.start[0] and \
                        self.empty_field[start][column] == "\u25A1":
                    return "Ships are too close"
                # Checking cell under the ship
                if end != ships.end[0] and \
                        self.empty_field[end][column] == "\u25A1":
                    return "Ships are too close"

                for r in range(start, ships.end[0] + 2):
                    try:
                        if self.empty_field[r][column + 1] == "\u25A1" \
                                or self.empty_field[[r][column - 1]] \
                                == "\u25A1":
                            return "Ships are too close"
                    except IndexError:
                        continue
        return

    def _validate_field(self):
        checking_ship_distance = self.checking_ship_distance()
        total_ships = 0
        for key, value in self.total_ships.items():
            total_ships += value
            if key == 4 and value != 1:
                return "You should have 1 four-deck ship"
            if key == 3 and value != 2:
                return "You should have 2 three-deck ships"
            if key == 2 and value != 3:
                return "You should have 3 two-deck ships"
            if key == 1 and value != 4:
                return "You should have 4 one-deck ships"
        if total_ships != 10:
            return "You should have 10 ships"
        if checking_ship_distance is None:
            return "Ships are OK"
        return checking_ship_distance
