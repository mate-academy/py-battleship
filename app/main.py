class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    total_number_of_ships = 0
    ships_type = {1: 0, 2: 0, 3: 0, 4: 0}

    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        if start[0] - end[0] != 0:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))
        if end[1] - start[1] != 0:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))

        Ship.total_number_of_ships += 1
        Ship.ships_type[len(self.decks)] += 1

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field()

    def fire(self, location: tuple):
        if location in self.field.keys():
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def _validate_field(self):
        if Ship.total_number_of_ships != 10:
            raise ValueError("The total number of the ships should be 10")
        if Ship.ships_type[1] != 4:
            raise ValueError("There should be 4 single-deck ships")
        if Ship.ships_type[2] != 3:
            raise ValueError("There should be 3 double-deck ships")
        if Ship.ships_type[3] != 2:
            raise ValueError("There should be 2 tree-deck ships")
        if Ship.ships_type[4] != 1:
            raise ValueError("There should be 2 four-deck ship")

        for cell, ship in self.field.items():
            for close_cell, close_ship in self.field.items():
                distance_between_cells = self.distance(cell, close_cell)
                if ship != close_ship and distance_between_cells < 2:
                    raise ValueError("Ships shouldn't be located "
                                     "in the neighboring cells!")

    @staticmethod
    def distance(first, second):
        row_sub = first[0] - second[0]
        column_sub = first[1] - second[1]
        return (row_sub ** 2 + column_sub ** 2) ** 0.5

    def print_field(self):
        for i in range(10):
            string = ""
            for j in range(10):
                current_cell = (i, j)
                if current_cell in self.field.keys():
                    current_ship = self.field[current_cell]
                    if current_ship.is_drowned is True:
                        string += "x\t"
                    elif current_ship.get_deck(i, j).is_alive is False:
                        string += "*\t"
                    else:
                        string += "□\t"
                else:
                    string += "~\t"
            print(string)
