class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks = []
        if start[0] == end[0] and start[1] == end[1]:
            self.decks.append(Deck(start[0], end[1]))
        elif start[0] == end[0]:
            for column_number in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column_number))
        elif start[1] == end[1]:
            for row_number in range(start[0], end[0] + 1):
                self.decks.append(Deck(row_number, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for desk in self.decks:
            if desk.row == row and desk.column == column:
                return desk

    def fire(self, row: int, column: int) -> str:
        fire_desk = self.get_deck(row, column)
        fire_desk.is_alive = False
        for desk in self.decks:
            if desk.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def _validate_field(self) -> None:
        ships = set([ship for ship in self.field.values()])
        deck_ships = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship in ships:
            deck_ships[len(ship.decks)] += 1
            for row in range(ship.start[0] - 1, ship.start[0] + 2, 2):
                for column in range(ship.start[1] - 1, ship.start[1] + 2, 2):
                    if ((row, column) in self.field) \
                            and (self.field[(row, column)] != ship):
                        print("ships shouldn't be located "
                              "in the neighboring cells")
            for row in range(ship.end[0] - 1, ship.end[0] + 2, 2):
                for column in range(ship.end[1] - 1, ship.end[1] + 2, 2):
                    if ((row, column) in self.field) \
                            and (self.field[(row, column)] != ship):
                        print("ships shouldn't be located "
                              "in the neighboring cells")
        if deck_ships != {4: 1, 3: 2, 2: 3, 1: 4}:
            print("the total number of the ships should be 10:\n"
                  "there should be 4 single-deck ships;\n"
                  "there should be 3 double-deck ships;\n"
                  "there should be 2 three-deck ships;\n"
                  "there should be 1 four-deck ship;")

    def __init__(self, ships: list) -> None:
        self.field = {}
        for tuple_ship in ships:
            ship = Ship(tuple_ship[0], tuple_ship[1])
            if len(ship.decks) == 1:
                self.field[tuple_ship[0]] = ship
            else:
                for deck in ship.decks:
                    self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) not in self.field:
                    print("~", end="\t")
                elif self.field[(row, column)].is_drowned:
                    print("x", end="\t")
                elif self.field[(row, column)].get_deck(row, column).is_alive:
                    print("□", end="\t")
                else:
                    print("*", end="\t")
            print("\n")
