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
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(deck.is_alive is False for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            ship = Ship(ship[0], ship[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field.get((row, column))
                    if ship.is_drowned:
                        print("x", end=" ")
                    else:
                        if ship.get_deck(row, column).is_alive:
                            print(u"\u25A1", end=" ")
                        else:
                            print("*", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        ships = list(self.field.values())
        count_decks_for_ship = {ship: ships.count(ship) for ship in ships}
        decks_values = list(count_decks_for_ship.values())
        if ((len(count_decks_for_ship) != 10
             or decks_values.count(1) != 4
             or decks_values.count(2) != 3
             or decks_values.count(3) != 2)
                or decks_values.count(4) != 1):
            raise ValueError("Invalid number or configuration of ships.")

        for deck1, ship1 in self.field.items():
            for deck2, ship2 in self.field.items():
                if ship1 != ship2:
                    if (abs(deck1[0] - deck2[0]) < 2
                            and abs(deck1[1] - deck2[1]) < 2):
                        raise ValueError("Ships should not be "
                                         "located in neighboring cells.")
