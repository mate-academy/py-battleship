class FleetSize(Exception):
    print("Total number of the ships should be 10")


class FleetMaintenanceShouldBeCorrect(Exception):
    print("In fleet should be 4 single-deck ships, 3 double-deck ships, "
          "2 three-deck ships, 1 four-deck ship")


class FleetLocate(Exception):
    print("ships shouldn't be located in the neighboring cells "
          "(even if cells are neighbors by diagonal)")


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.coordinate = self.check_coordinate(start, end)
        self.decks = self.create_ship()
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False
        alive_deck = [deck.is_alive for deck in self.decks]

        if any(alive_deck):
            return "Hit!"
        else:
            self.is_drowned = True
            return "Sunk!"

    def create_ship(self):
        return [Deck(coordinate[0], coordinate[1])
                for coordinate in self.coordinate]

    @staticmethod
    def check_coordinate(start, end):
        x1, y1 = start
        x2, y2 = end
        coordinates = []
        if x1 != x2:
            ship_length = x2 - x1
            for i in range(ship_length + 1):
                coordinates.append((x1 + i, y1))
        else:
            ship_length = y2 - y1
            for i in range(ship_length + 1):
                coordinates.append((x1, y1 + i))
        return coordinates


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        ships_for_checking = []

        for ship in ships:
            ship = Ship(ship[0], ship[1])
            for coordinate in ship.coordinate:
                self.field[coordinate] = ship
            ships_for_checking.append(ship)

        self._validate_field(ships_for_checking)

    def _validate_field(self, ships):
        if len(ships) != 10:
            raise FleetSize
        check_fleet_maintenance = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }

        for ship in ships:
            check_fleet_maintenance[len(ship.decks)] += 1
        if check_fleet_maintenance != {
            1: 4,
            2: 3,
            3: 2,
            4: 1,
        }:
            raise FleetMaintenanceShouldBeCorrect

        for ship in ships:
            for coordinate in ship.coordinate:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        check_coordinate = (
                            coordinate[0] + i,
                            coordinate[1] + j
                        )
                        if check_coordinate in self.field:
                            find_ship = self.field[coordinate]
                            if find_ship != ship:
                                raise FleetLocate

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        self.print_field()
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        else:
            return "Miss!"

    def print_field(self):
        for i in range(10):
            for j in range(10):
                if (i, j) in self.field:
                    ship = self.field[(i, j)]
                    if ship.is_drowned:
                        print("x", end=" ")
                    else:
                        deck = ship.get_deck(i, j)
                        if deck.is_alive:
                            print("@", end=" ")
                        else:
                            print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
        print()
