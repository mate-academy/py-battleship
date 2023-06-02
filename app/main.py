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
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for desk in self.decks:
            if desk.row == row and desk.column == column:
                return desk

    def fire(self, row: int, column: int) -> str:
        fire_desk = self.get_deck(row, column)
        if fire_desk is None:
            return "Miss!"
        fire_desk.is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)
        if self.is_drowned:
            return "Sunk!"
        return "Hit!"


class Battleship:
    def check_neighbor_cells(self, ship: Ship, ship_desk: tuple) -> None:
        for row in range(ship_desk[0] - 1, ship_desk[0] + 2, 2):
            for column in range(ship_desk[1] - 1, ship_desk[1] + 2, 2):
                if ((row, column) in self.field) \
                        and (self.field[(row, column)] != ship):
                    raise ValueError("ships shouldn't be located "
                          "in the neighboring cells")

    def _validate_field(self) -> None:
        ships = set([ship for ship in self.field.values()])
        deck_ships = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship in ships:
            deck_ships[len(ship.decks)] += 1
            self.check_neighbor_cells(ship, ship.start)
            self.check_neighbor_cells(ship, ship.end)
        if deck_ships != {4: 1, 3: 2, 2: 3, 1: 4}:
            raise ValueError(
                "the total number of the ships should be 10:\n"
                "there should be 4 single-deck ships;\n"
                "there should be 3 double-deck ships;\n"
                "there should be 2 three-deck ships;\n"
                "there should be 1 four-deck ship;"
            )

    def __init__(self, ships: list) -> None:
        self.field = {}
        for tuple_ship in ships:
            ship = Ship(tuple_ship[0], tuple_ship[1])
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
