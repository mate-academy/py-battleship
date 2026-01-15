from __future__ import annotations


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self,
                 row: int,
                 column: int
                 ) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self,
             row: int,
             column: int
             ) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]
                 ) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.coord_to_ship = {}
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "□"
                self.coord_to_ship[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, ceil: tuple[int]) -> str:
        if ceil not in self.coord_to_ship:
            return "Miss!"
        ship = self.coord_to_ship[ceil]
        ship.fire(ceil[0], ceil[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                ship = self.coord_to_ship.get((row, column))
                if ship:
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("x", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            deck_count = len(ship.decks)
            if deck_count > 4:
                raise ValueError("Ship with more than 4 decks is not allowed.")
            ship_counts[deck_count] += 1
        if ship_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Ship distribution is invalid.")
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships.")
        for ship in self.ships:
            for deck in ship.decks:
                if self.is_neighboring_ships(deck):
                    raise ValueError(f"Ships are located in "
                                     f"neighboring cells near "
                                     f"({deck.row}, {deck.column}).")

    def is_neighboring_ships(self, deck: Deck) -> bool:
        row, col = deck.row, deck.column
        for r_ in range(row - 1, row + 2):
            for c_ in range(col - 1, col + 2):
                if (r_, c_) != (row, col) and 0 <= r_ < 10 and 0 <= c_ < 10:
                    if (r_, c_) in self.coord_to_ship:
                        neighboring_ship = self.coord_to_ship[(r_, c_)]
                        if neighboring_ship != self.coord_to_ship[(row, col)]:
                            return True
        return False
