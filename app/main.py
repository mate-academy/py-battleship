import math


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    total_ships_number = 0
    ships_type = {1: 0, 2: 0, 3: 0, 4: 0}

    def __init__(self, start, end, is_drowned=False):
        self.decks = {start: Deck(start[0], start[1])}
        self.all_deck_of_ship(start, end)
        self.is_drowned = is_drowned
        Ship.total_ships_number += 1
        Ship.ships_type[len(self.decks)] += 1

    def all_deck_of_ship(self, start, end):
        if start != end:
            if start[0] != end[0] and start[1] == end[1]:
                for i in range(start[0] + 1, end[0]):
                    self.decks[(i, start[1])] = Deck(i, start[1])
            elif start[1] != end[1] and start[0] == end[0]:
                for i in range(start[1] + 1, end[1]):
                    self.decks[(start[0], i)] = Deck(start[0], i)
            else:
                raise ValueError(
                    f"Ship ({start}, {end})can`t be located by diagonal!"
                )
            self.decks[end] = Deck(end[0], end[1])

    def get_deck(self, row, column):
        self.fire(row, column)
        if self.is_drowned is True:
            return "Sunk!"
        return "Hit!"

    def fire(self, row, column):
        self.decks[(row, column)].is_alive = False
        if not any([deck.is_alive for deck in self.decks.values()]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):

        self.field = {}
        for ship in ships:
            current_ship = Ship(ship[0], ship[1])
            for deck in current_ship.decks.keys():
                self.field[deck] = current_ship

    def fire(self, location: tuple):
        if location in self.field:
            return self.field[location].get_deck(location[0], location[1])
        return "Miss!"

    def print_field(self):
        for row in range(10):
            str_to_print = ""
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = self.field[(row, column)].decks[(row, column)]
                    if ship.is_drowned:
                        str_to_print += "x"
                    elif not deck.is_alive:
                        str_to_print += "*"
                    else:
                        str_to_print += "□"
                else:
                    str_to_print += "~"
            print("  ".join(str_to_print))

    def _validate_field(self):
        if Ship.total_ships_number != 10:
            print("The total number of the ships should be 10!")
        if Ship.ships_type[1] != 4:
            print("There should be 4 single-deck ships")
        if Ship.ships_type[2] != 3:
            print("There should be 3 double-deck ships")
        if Ship.ships_type[3] != 2:
            print("There should be 2 tree-deck ships")
        if Ship.ships_type[4] != 1:
            print("There should be 2 four-deck ship")

        for deck, ship in self.field.items():
            for compare_deck, compare_ship in self.field.items():
                distance_to_deck = self.distance(deck, compare_deck)
                if ship != compare_ship and distance_to_deck < 2:
                    print(
                        "Ships shouldn't be located in the neighboring cells!"
                    )
                    return

    @staticmethod
    def distance(first, second):
        x_sub = first[0] - second[0]
        y_sub = first[1] - second[1]
        return math.sqrt(x_sub ** 2 + y_sub ** 2)
