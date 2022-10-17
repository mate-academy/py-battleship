class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        if not (start[0] == end[0] or start[1] == end[1]):
            raise ValueError("Decks shouldn't be located "
                             "by diagonal)")

        self.start = start
        self.end = end
        self.decks = {(i, j): Deck(i, j)
                      for i in range(start[0], end[0] + 1)
                      for j in range(start[1], end[1] + 1)}
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks.values()):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = {(x, y): Ship(x, y) for x, y in ships}
        self.field = {}
        self.field.update({deck: ship
                           for ship in self.ships.values()
                           for deck in ship.decks.keys()})
        self._validate_field()

    def fire(self, location: tuple) -> str:

        if location not in self.field:
            return "Miss!"

        self.field[location].fire(*location)

        if self.field[location].is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(1, 11):
            for column in range(1, 11):
                point = (row, column)
                if self.field.get(point) is None:
                    print("~\t", end="")
                    continue
                if self.field[point].is_drowned:
                    print("x\t", end="")
                    continue
                if not self.field[point].decks[point].is_alive:
                    print("*\t", end="")
                else:
                    print(u"\u25A1" + "\t", end="")
            print("\n")

    def _validate_ships_count(self) -> None:
        # validate data is dict{decks: count of ship}
        correct = {4: 1, 3: 2, 2: 3, 1: 4}
        current = {4: 0, 3: 0, 2: 0, 1: 0}

        for ship in self.ships.values():
            current[len(ship.decks)] += 1

        if current != correct:
            raise ValueError("Wrong count of ships")

    def _validate_ships_location(self) -> None:
        blocked_points = set()
        for ship in self.ships.values():

            for point in ship.decks.keys():
                if point in blocked_points:
                    raise ValueError("ships shouldn't be "
                                     "located in the neighboring cells")

            for point_x in range(min(ship.start[0], ship.end[0]) - 1,
                                 max(ship.start[0], ship.end[0]) + 2):

                for point_y in range(min(ship.start[1], ship.end[1]) - 1,
                                     max(ship.start[1], ship.end[1]) + 2):

                    blocked_points.add((point_x, point_y))

    def _validate_field(self) -> None:
        self._validate_ships_count()
        self._validate_ships_location()
