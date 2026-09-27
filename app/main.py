class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def _calc(self, num: int) -> list:
        points = []
        if self.start[num] > self.end[num]:
            for i in range(self.start[num] - self.end[num] + 1):
                poi = self.end[num] + i
                points.append(poi)
        else:
            for i in range(self.end[num] - self.start[num] + 1):
                poi = self.start[num] + i
                points.append(poi)
        return points

    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        if start[0] != end[0]:
            points = self._calc(0)
            for point in points:
                self.decks.append(Deck(row=point, column=start[1]))
        elif start[1] != end[1]:
            points = self._calc(1)
            for point in points:
                self.decks.append(Deck(row=start[0], column=point))

        else:
            self.decks.append(Deck(row=start[0], column=start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row=row, column=column)
        if deck:
            deck.is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False
                break
        else:
            self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field = {}
        for ship_coords in ships:
            ship = Ship(start=ship_coords[0], end=ship_coords[1])
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError("Ships cannot occupy the same cell")

                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship: Ship = self.field[location]
            ship.fire(row=location[0], column=location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for column in range(10):
                if (row, column) in self.field:
                    ship: Ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        line += "□"
                    elif not ship.is_drowned:
                        line += "*"
                    else:
                        line += "x"
                else:
                    line += "~"
            print(line)

    def _validate_field(self) -> None:
        one = 0
        two = 0
        three = 0
        four = 0
        ships = []

        for deck in self.field:
            ship = self.field[deck]
            if ship not in ships:
                ships.append(ship)

                if len(ship.decks) == 1:
                    one += 1
                elif len(ship.decks) == 2:
                    two += 1
                elif len(ship.decks) == 3:
                    three += 1
                elif len(ship.decks) == 4:
                    four += 1

        if one != 4 or two != 3 or three != 2 or four != 1 or len(ships) != 10:
            raise ValueError

        for (row, column), ship in self.field.items():
            for row_shift in range(-1, 2):
                for column_shift in range(-1, 2):
                    if row_shift == 0 and column_shift == 0:
                        continue

                    neighbour = (
                        row + row_shift,
                        column + column_shift,
                    )
                    neighbour_ship = self.field.get(neighbour)

                    if (
                        neighbour_ship is not None
                        and neighbour_ship is not ship
                    ):
                        raise ValueError(
                            "Ships are located in neighboring cells"
                        )
