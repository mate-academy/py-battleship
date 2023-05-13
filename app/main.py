class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive: bool = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.is_drowned: bool = False
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self._area = [[" - " for _ in range(10)] for _ in range(10)]
        self._miss_fire = []
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        self._miss_fire.append(location)
        return "Miss!"

    def print_field(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    self._area[deck.row][deck.column] = " # "
                elif deck.is_alive:
                    self._area[deck.row][deck.column] = " □ "
                else:
                    self._area[deck.row][deck.column] = " X "
        for miss in self._miss_fire:
            self._area[miss[0]][miss[1]] = " * "
        for area in self._area:
            print("\t".join(str(cell) for cell in area))

    def _validate_field(self) -> None:
        if len(set(self.field.values())) != 10:
            raise ValueError("The total number of ships is not 10")
        expected_ship_types = {1: 4, 2: 3, 3: 2, 4: 1}
        ships_types = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in set(self.field.values()):
            if len(ship.decks) == 1:
                ships_types[1] += 1
            if len(ship.decks) == 2:
                ships_types[2] += 1
            if len(ship.decks) == 3:
                ships_types[3] += 1
            if len(ship.decks) == 4:
                ships_types[4] += 1
        if ships_types != expected_ship_types:
            raise ValueError("Incorrect number of ships of different types")
        for ship_1 in self.field.values():
            for ship_2 in self.field.values():
                if ship_1 != ship_2:
                    for deck_1 in ship_1.decks:
                        for deck_2 in ship_2.decks:
                            if abs(deck_1.row - deck_2.row) <= 1 and \
                                    abs(deck_1.column - deck_2.column) <= 1:
                                raise ValueError(
                                    "The ships cannot be placed in "
                                    "adjacent squares (including diagonally)"
                                )
