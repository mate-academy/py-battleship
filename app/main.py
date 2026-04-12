class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if self.start[0] == self.end[0]:
            self.deck = [Deck(self.start[0], length) for length in range(self.start[1], self.end[1] + 1)]
        else:
            self.deck = [Deck(length, self.start[1]) for length in range(self.start[0], self.end[0] + 1)]

        self.count_alive = len(self.deck)

    def get_deck(self, row: int, column: int):
        return self.deck.index(Deck(row, column))

    def fire(self, row: int, column: int) -> str:
        shot_place = self.get_deck(row, column)
        if self.deck[shot_place].is_alive:
            self.deck[shot_place].is_alive = False
            self.count_alive -= 1
        if not self.count_alive:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]):
        self.field = {}
        self.missed = set()
        for ship in ships:
            start, end = ship[0], ship[1]
            if start[0] > end[0] or start[1] > end[1]:
                start, end = ship[1], ship[0]

            if start[0] != end[0] and start[1] != end[1]:
                raise ValueError("Ships can be placed only straight in row or column")
            ship_instance = Ship(start, end)
            if start[1] == end[1]:
                self.field.update({(point, start[1]) : ship_instance for point in range(start[0], end[0] + 1)})
            else:
                self.field.update({(start[0], point): ship_instance for point in range(start[1], end[1] + 1)})


    def fire(self, location: tuple):
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        else:
            self.missed.add(location)
            return "Miss!"


    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if not self.field[(row, column)].is_drowned:
                        ship = self.field[(row, column)]
                        if ship.deck[ship.get_deck(row, column)].is_alive:
                            print(u"\t\u25A1", end="")
                        else:
                            print("\t*", end="")
                    else:
                        print("\tX", end="")
                else:
                    if (row, column) in self.missed:
                        print("\tO", end="")
                    else:
                        print("\t~", end="")
            print()


battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)
battle_ship.print_field()

print(battle_ship.fire((0, 4)))
print(battle_ship.fire((0, 3)))
print(battle_ship.fire((0, 2)))
print(battle_ship.fire((0, 1)))
print(battle_ship.fire((0, 0)))
print(battle_ship.fire((9, 9)))
print(battle_ship.fire((4, 0)))
print(battle_ship.fire((9, 0)))
print(battle_ship.fire((7, 7)))
print(battle_ship.fire((6, 6)))

battle_ship.print_field()
