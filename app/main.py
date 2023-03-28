from math import dist


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self._distance = int(dist(end, self.start))
        self.decks = self._deck_builder()
        self.is_drowned = is_drowned

    def _deck_builder(self) -> list:
        if self.start == self.end:
            decks = [Deck(self.start[0], self.start[1])]
        elif self.start[0] == self.end[0]:
            decks = [Deck(
                self.start[0], self.start[1] + number
            ) for number in range(self._distance + 1)]
        else:
            decks = [Deck(
                self.start[0] + number, self.start[1]
            ) for number in range(self._distance + 1)]
        return decks

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck.is_alive

    def fire(self, row: int, column: int) -> None:
        counter = 0
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
            if not deck.is_alive:
                counter += 1

        if len(self.decks) == counter:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            self.print_field()
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        self.print_field()
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    if self.field[(row, col)].is_drowned:
                        print("x ", end="")
                    elif not self.field[(row, col)].get_deck(row, col):
                        print("* ", end="")
                    else:
                        print("□ ", end="")
                else:
                    print("~ ", end="")
            print()
