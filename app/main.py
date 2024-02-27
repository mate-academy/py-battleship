class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks = [Deck(start[0], start[1])]
        if start[0] == end[0]:
            self.decks = [Deck(start[0], start[1] + i)
                          for i in range(abs(start[1] - end[1]) + 1)]
        if start[1] == end[1]:
            self.decks = [Deck(start[0] + i, end[1])
                          for i in range(abs(start[0] - end[0]) + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column and deck.is_alive:
                return deck

    def fire(self, row: int, column: int) -> int:
        attacked_deck = self.get_deck(row, column)
        attacked_deck.is_alive = False
        if not all(self.decks):
            self.is_drowned = True
        return sum(deck.is_alive for deck in self.decks)


class Battleship:

    def _validate_field(self, ship: tuple[tuple, tuple]) -> None:
        if sum(self.fleet.values()) > 10:
            raise ValueError("The total number of the ships should be 10")
        count_deck = abs(
            (ship[1][0] - ship[0][0]) - (ship[1][1] - ship[0][1])) + 1
        if count_deck == 1:
            self.fleet["single_deck"] += 1
        elif count_deck == 2:
            self.fleet["double_deck"] += 1
        elif count_deck == 3:
            self.fleet["three_deck"] += 1
        elif count_deck == 4:
            self.fleet["four_deck"] += 1
        if self.fleet["single_deck"] > 4:
            raise ValueError("there should be 4 single-deck ships")
        if self.fleet["double_deck"] > 3:
            raise ValueError("there should be 3 double-deck ships")
        if self.fleet["three_deck"] > 2:
            raise ValueError("there should be 2 three-deck ships")
        if self.fleet["four_deck"] > 1:
            raise ValueError("there should be 1 four-deck ship")
        for row in range(ship[0][0] - 1, ship[1][0] + 2):
            for column in range(ship[0][1] - 1, ship[1][1] + 2):
                if (row, column) in self.field:
                    raise ValueError("Ships should not be located in "
                                     "neighboring cells")

    def __init__(self, ships: list[tuple[tuple, tuple]] | None = None) -> None:
        self.fleet = {
            "single_deck": 0, "double_deck": 0, "three_deck": 0,
            "four_deck": 0
        }
        self.field = {}
        if ships is not None:
            for coordinates_ship in ships:
                self._validate_field(coordinates_ship)
                ship = Ship(coordinates_ship[0], coordinates_ship[1])
                for deck in ship.decks:
                    self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            self.field[location] = "Miss!"
            return "Miss!"
        else:
            ship = self.field[location]
            fire = ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Drowned!"
            if fire == 0:
                return "Sunk!"
            self.field[location] = "X"
            return "Hit!"

    def print_field(self):
        game_field = [["\U0001F7E6"] * 10 for _ in range(10)]
        for ceil in self.field:
            if self.field[ceil] == "Miss!":
                game_field[ceil[0]][ceil[1]] = "\u274C"
            elif self.field[ceil] == "X":
                game_field[ceil[0]][ceil[1]] = "\U0001F525"
            else:
                game_field[ceil[0]][ceil[1]] = "\u26F5"
        for row in game_field:
            print(*row)
        print("-" * 32)


# battle_ship = Battleship(
#     ships=[
#         ((0, 0), (0, 3)),
#         ((0, 5), (0, 6)),
#         ((0, 8), (0, 9)),
#         ((2, 0), (4, 0)),
#         ((2, 4), (2, 6)),
#         ((2, 8), (2, 9)),
#         ((9, 9), (9, 9)),
#         ((7, 7), (7, 7)),
#         ((7, 9), (7, 9)),
#         ((9, 7), (9, 7)),
#     ]
# )
# battle_ship.fire((0, 4)),  # Miss!
# battle_ship.print_field()
# battle_ship.fire((0, 3)),  # Hit!
# battle_ship.print_field()
# battle_ship.fire((0, 2)),  # Hit!
# battle_ship.print_field()
# battle_ship.fire((0, 1)),  # Hit!
# battle_ship.print_field()
# battle_ship.fire((0, 0)),  # Sunk!
# battle_ship.print_field()
