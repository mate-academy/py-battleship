class ShipError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, end[1]))
        elif start[0] == end[0] and start[1] == end[1]:
            self.decks.append(Deck(start[0], end[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> Deck:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def _add_cell_ship(self, row: tuple, column: tuple, ship: Ship) -> None:
        self.field[(row, column)] = ship
        self.desk[(row, column)] = "\u25A0"

    def _validate_field(self) -> None:
        len_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            if ship[0][0] != ship[1][0] and ship[0][1] != ship[1][1]:
                raise ShipError("Ship should place only "
                                "horizontally or vertically")
            if ship[1][1] - ship[0][1] > 4 or ship[1][0] - ship[0][0] > 4:
                raise ShipError("Ship should have 4 or lower decks")
            elif ship[1][1] - ship[0][1] == 0 and ship[1][0] - ship[0][0] == 0:
                len_ships[1] += 1
            elif ship[1][1] - ship[0][1] == 1 or ship[1][0] - ship[0][0] == 1:
                len_ships[2] += 1
            elif ship[1][1] - ship[0][1] == 2 or ship[1][0] - ship[0][0] == 2:
                len_ships[3] += 1
            elif ship[1][1] - ship[0][1] == 3 or ship[1][0] - ship[0][0] == 3:
                len_ships[4] += 1
        if len_ships[1] != 4:
            raise ShipError("There should be 4 single-deck ships")
        elif len_ships[2] != 3:
            raise ShipError("There should be 3 double-deck ships")
        elif len_ships[3] != 2:
            raise ShipError("There should be 2 three-deck ships")
        elif len_ships[4] != 1:
            raise ShipError("There should be 1 four-deck ships")

    def __init__(self, ships: dict) -> None:
        self.ships = ships
        self.desk = {}
        for row in range(10):
            for column in range(10):
                self.desk[(row, column)] = "\u25A1"
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            if ship[0][0] == ship[1][0]:
                for column in range(ship[0][1], ship[1][1] + 1):
                    self._add_cell_ship(ship[0][0], column, new_ship)
            elif ship[0][1] == ship[1][1]:
                for row in range(ship[0][0], ship[1][0] + 1):
                    self._add_cell_ship(row, ship[1][1], new_ship)
            elif ship[0][0] == ship[1][0] and ship[0][1] == ship[1][1]:
                self._add_cell_ship(ship[0][0], ship[0][1], new_ship)
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            if self.field[location].get_deck(location[0],
                                             location[1]).is_alive:
                self.field[location].fire(location[0], location[1])
                if self.field[location].is_drowned:
                    for deck in self.field[location].decks:
                        self.desk[(deck.row, deck.column)] = "X"
                    return "Sunk!"
                self.desk[location] = "*"
                return "Hit!"
            return "This cell shoted already"
        self.desk[location] = "\u2022"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            print()
            for column in range(10):
                print(self.desk[(row, column)], "   ", end="")
            print()
