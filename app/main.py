from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        if all([start[0] == end[0], abs(start[0] - end[0]) <= 4]):
            for column in (range(start[1], end[1] + 1)):
                self.decks.append(Deck(start[0], column))
        elif all([start[1] == end[1], abs(start[0] - end[0]) <= 4]):
            for row in (range(start[0], end[0] + 1)):
                self.decks.append(Deck(row, start[1]))
        else:
            raise ValueError("Ship length must be 1-4, and it must be strait")

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if len([deck for deck in self.decks if deck.is_alive]):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            battleship = Ship(*ship)
            for deck in battleship.decks:
                self.field[(deck.row, deck.column)] = battleship
        self._validate_field()

    def fire(self, location: tuple):
        try:
            if location in self.field:
                ship = self.field[location]
                return ship.fire(location[0], location[1])
            else:
                return "Miss!"
        finally:
            self.print_field()

    def print_field(self):
        for row in range(10):
            line = ""
            for colum in range(10):
                if (row, colum) in self.field:
                    if self.field[(row, colum)].get_deck(row, colum).is_alive:
                        line += " □ "
                    elif self.field[(row, colum)].is_drowned:
                        line += " x "
                    else:
                        line += " * "
                else:
                    line += " ~ "
            print(line)
        print("\n")

    def _validate_field(self):
        if len(set(self.field.values())) != 10:
            raise ValueError("You must provide 10 ships")
        ships = [len([k for k, v in self.field.items() if v == i])
                 for i in set(self.field.values())]
        count_of_ships = {ship: ships.count(ship) for ship in set(ships)}
        if count_of_ships != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("there should be 4 single-deck ships"
                             "there should be 3 double-deck ships"
                             "there should be 2 three-deck ships"
                             "there should be 1 four-deck ship")
        for coord in self.field:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    check_point = (coord[0] + x, coord[1] + y)
                    if check_point in self.field and \
                            self.field[check_point] != self.field[coord]:
                        raise ValueError("ships shouldn't be located "
                                         "in the neighboring cells")
