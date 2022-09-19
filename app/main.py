import math


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
        self.save_deck()

    def save_deck(self):
        if self.start[0] == self.end[0]:
            length = self.end[1] - self.start[1]
            for idx in range(length + 1):
                self.decks.append(Deck(self.start[0], self.start[1] + idx))
        elif self.start[1] == self.end[1]:
            length = self.end[0] - self.start[0]
            for idx in range(length + 1):
                self.decks.append(Deck(self.start[0] + idx, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        self.check_alive()

    def check_alive(self):
        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = dict()
        self.save_field()
        self._validate_field()

    def save_field(self):
        """This method assign a ship to every cell(e.g. deck)"""

        for ship in self.ships:
            ship_cell = Ship(ship[0], ship[1])
            if ship[0][0] == ship[1][0]:
                length = ship[1][1] - ship[0][1]
                for idx in range(length + 1):
                    self.field[(ship[0][0], ship[0][1] + idx)] \
                        = ship_cell
            elif ship[0][1] == ship[1][1]:
                length = ship[1][0] - ship[0][0]
                for idx in range(length + 1):
                    self.field[(ship[0][0] + idx, ship[1][1])] \
                        = ship_cell

    def fire(self, location: tuple):
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        else:
            return "Miss!"

    def ships_on_field(self):
        """This method create a matrix 10x10 aka field with ships
        that corresponds to specific symbols. ~ - empty cell, □ - deck alive,
        * - damaged ship, x - killed ship"""
        new_field = [["~" for i in range(10)] for i in range(10)]
        for deck in self.field.keys():
            new_field[deck[0]][deck[1]] = u"\u25A1"
            if not self.field[deck].get_deck(deck[0], deck[1]).is_alive:
                new_field[deck[0]][deck[1]] = "*"
                if self.field[deck].is_drowned:
                    new_field[deck[0]][deck[1]] = "x"
        return new_field

    def print_field(self):
        new_field = self.ships_on_field()
        for ele in new_field:
            print('\t'.join(ele))

    @staticmethod
    def distance(ship):
        return math.sqrt((ship[1][0] - ship[0][0])**2
                         + (ship[1][1] - ship[0][1])**2)

    def _validate_field(self):
        input_ships = sorted([self.distance(ship)
                              + 1 for ship in self.ships], reverse=True)

        if len(input_ships) != 10:
            raise Exception("The total number of the ships should be 10!")
        elif 4.0 not in input_ships:
            raise Exception("There should be 1 four-deck ship!")
        elif [3.0, 3.0] != input_ships[1:3]:
            raise Exception("There should be 2 three-deck ship!")
        elif [2.0, 2.0, 2.0] != input_ships[3:6]:
            raise Exception("There should be 3 double-deck ship!")
        elif [1.0, 1.0, 1.0, 1.0] != input_ships[6:]:
            raise Exception("There should be 4 single-deck ship!")

        """For each ship we book cells around and raise exception
         if next ship trying to locate in booked cells."""
        booked_cells_field = []
        ship_check = None
        for deck in self.field.keys():
            booked_cells = self.used_cells_deck(deck)
            if not booked_cells_field:
                booked_cells_field += booked_cells
            elif deck in booked_cells_field and \
                    self.field[deck] != ship_check:
                raise Exception(f"Find new place for the ship "
                                f"with coordinates that starts "
                                f"{self.field[deck].start} and ends"
                                f" {self.field[deck].end}")
            intersection = list(set(booked_cells) - set(booked_cells_field))
            ship_check = self.field[deck]
            booked_cells_field += intersection

    @staticmethod
    def used_cells_deck(deck):
        """For each deck we book all cells
         around and discard repeated values."""
        used_cells = [[[deck[0] + j, deck[1] + i]
                       for i in range(-1, 2)] for j in range(-1, 2)]
        booked_cells = []
        for cell in used_cells:
            booked_cells += cell

        for cell in booked_cells:
            for idx, cor in enumerate(cell):
                if cor == -1:
                    cell[idx] = 0
        return list(set(map(tuple, booked_cells)))
