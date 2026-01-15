from exeptions.ship_exeptions import (FieldLocations, ShipLocations,
                                      ShipsCounts, ShipsByDecks)


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        def validate_location(row: int, column: int) -> bool:
            if 0 <= row < 10 and 0 <= column < 10:
                return True
            return False

        self.decks = []

        if validate_location(*start) and validate_location(*end):
            if start[0] == end[0]:
                for y in range(start[1], end[1] + 1):
                    self.decks.append(Deck(start[0], y))
            elif start[1] == end[1]:
                for x in range(start[0], end[0] + 1):
                    self.decks.append(Deck(x, start[1]))

        self.is_drowned = is_drowned

    def get_deck(self, row, column) -> Deck:
        return [self.decks[i] for i, deck in enumerate(self.decks) if
                deck.row == row and deck.column == column][0]

    def fire(self, row, column):
        deck = self.get_deck(row, column)

        if deck is not None:
            if deck.is_alive:
                deck.is_alive = False
                self.is_drowned = True
                for check in self.decks:
                    if check.is_alive:
                        self.is_drowned = False
                        break
                if not self.is_drowned:
                    return "Hit!"

        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        self._deck_of_ships = [0, 0, 0, 0]

        for ship_location in ships:
            ship = Ship(ship_location[0], ship_location[1])

            if len(ship.decks) > 0:
                self._deck_of_ships[len(ship.decks) - 1] += 1
            start, end = ship_location

            if start[0] == end[0]:
                for y in range(start[1], end[1] + 1):
                    self.field[(start[0], y)] = ship

            elif start[1] == end[1]:
                for x in range(start[0], end[0] + 1):
                    self.field[(x, start[1])] = ship

        self._validate_field()

    def fire(self, location: tuple):
        try:
            ship = self.field[location]
        except KeyError:
            return "Miss!"

        row, column = location
        return ship.fire(row, column)

    def get_ship_by_location(self, row, column) -> (Ship, None):
        try:
            return self.field[(row, column)]
        except KeyError:
            return None

    def print_field(self):
        line = "        "
        for column in range(10):
            line += f"  {column}    "
        print(line)

        for row in range(10):
            line = f"   {row}   "
            for column in range(10):
                deck = None
                ship = self.get_ship_by_location(row, column)
                if ship is not None:
                    deck = ship.get_deck(row, column)

                if deck is not None:
                    if deck.is_alive:
                        line += "   □   "
                        continue
                    else:
                        line += "   *   "
                        continue
                line += "       "

            print(line + "\n")

    def _validate_field(self):
        for ship in self.field.values():
            for deck in ship.decks:
                for rows in range(-1, 2):
                    for column in range(-1, 2):
                        neighbouring_ship = self.get_ship_by_location(
                            deck.row + rows, deck.column + column)
                        if neighbouring_ship is not None and \
                                neighbouring_ship != ship:
                            raise ShipLocations

        if sum(self._deck_of_ships) != 10:
            raise ShipsCounts

        if self._deck_of_ships != [4, 3, 2, 1]:
            raise ShipsByDecks


def small_battle_ship_game():
    # It's not for delete, because it's small battleship game. :)
    try:
        sea = Battleship([((2, 0), (2, 3)),
                          ((4, 5), (4, 6)),
                          ((3, 8), (3, 9)),
                          ((6, 0), (8, 0)),
                          ((6, 4), (6, 6)),
                          ((6, 8), (6, 9)),
                          ((9, 9), (9, 9)),
                          ((9, 5), (9, 5)),
                          ((9, 3), (9, 3)),
                          ((9, 7), (9, 7))])
    except FieldLocations as e:
        print(e)
        return

    while True:
        sea.print_field()
        location = input("Input coordinates for fire: ")
        if location.lower() in ["exit", "quit", "q", "close"]:
            break
        try:
            if "," in location:
                row, columns = location.split(",")
            else:
                row, columns = location.split()
            if 0 < int(row) > 9 or 0 < int(columns) > 9:
                raise ValueError
        except ValueError:
            print("Wrong coordinates. Repeat please.")
            continue
        print(sea.fire((int(row), int(columns))))
