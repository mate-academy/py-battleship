class NumberOfShipsDeck(Exception):
    pass


class TotalNumberOfTheShips(Exception):
    pass


class Deck:
    def __init__(self, row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.coordinates_ships = []
        self.check_vertical_deck()
        self.create_ship()

    def check_vertical_deck(self) -> None:
        if self.start[0] != self.end[0]:
            for coord in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(coord, self.end[1]))
                self.coordinates_ships.append(Deck(coord, self.end[1]))

    def create_ship(self) -> None:
        if len(self.decks) == 0:
            for coord in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], coord))
                self.coordinates_ships.append(Deck(self.start[0], coord))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        ship_deck = self.get_deck(row, column)
        ship_deck.is_alive = False

        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.fields = {}
        self.calculate_ships()
        self._validate_field()

    def _validate_field(self) -> None:
        if not len(self.ships) == 10:
            raise TotalNumberOfTheShips("Total number ships should be 10")

        ships_ok = {"single_deck_ship": 4,
                    "double_deck_ship": 3,
                    "three_deck_ship": 2,
                    "four_deck_ship": 1}

        ships = {"single_deck_ship": 0,
                 "double_deck_ship": 0,
                 "three_deck_ship": 0,
                 "four_deck_ship": 0}

        for ship in self.ships:
            len_deck = Ship(ship[0], ship[1])
            if len(len_deck.decks) == 4:
                ships["four_deck_ship"] += 1
            elif len(len_deck.decks) == 3:
                ships["three_deck_ship"] += 1
            elif len(len_deck.decks) == 2:
                ships["double_deck_ship"] += 1
            else:
                ships["single_deck_ship"] += 1

        if ships_ok != ships:
            raise NumberOfShipsDeck("In game you should have "
                                    "4 single_deck_ship, "
                                    "3 double_deck_ship, "
                                    "2 three_deck_ship, "
                                    "1 four_deck_ship")

    def calculate_ships(self) -> None:
        for ship in self.ships:
            num_ship = Ship(ship[0], ship[1])

            for deck in num_ship.decks:
                self.fields[(deck.row, deck.column)] = num_ship

    def battle_map(self) -> list:
        map_ = []
        for row in range(10):
            a_cell = ""
            for column in range(10):
                ship = self.fields.get((row, column), None)
                if ship is None:
                    a_cell += "~"
                elif ship.is_drowned:
                    a_cell += "x"
                elif not ship.get_deck(row, column).is_alive:
                    a_cell += "*"
                else:
                    a_cell += u"\u25A1"
            map_.append(a_cell)
        return map_

    def print_fields(self) -> None:
        for row in self.battle_map():
            print((" " * 6).join(map(str, row)))

    def fire(self, location: tuple) -> str:
        ship = self.fields.get(location, None)
        if ship is not None:
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
