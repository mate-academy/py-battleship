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
        self.decks = (
            [
                Deck(row, column)
                for row in range(self.start[0], self.end[0] + 1)
                for column in range(self.start[1], self.end[1] + 1)
            ]
        )

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str | None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(deck.is_alive is False for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            ship = Ship(ship[0], ship[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        return (
            self.field[location[0], location[1]].fire(location[0], location[1])
        )

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field.keys():
                    ship = self.field.get((row, column))
                    if ship.is_drowned:
                        print("  X  ", end="")
                    else:
                        if ship.get_deck(row, column).is_alive:
                            print("  O  ", end="")
                        else:
                            print("  *  ", end="")
                else:
                    print("  ~  ", end="")
            print("\n")

    def _validate_field(self) -> None:
        ships = [ship for ship in self.field.values()]
        ship_count = {ship: ships.count(ship) for ship in ships}
        ship_count_values = [value for value in ship_count.values()]
        if len(ship_count) != 10:
            raise Exception("The total number of the ships should be 10")
        for _ in ship_count_values:
            if ship_count_values.count(1) != 4:
                raise Exception("There should be 4 single-deck ships")
            if ship_count_values.count(2) != 3:
                raise Exception("There should be 3 single-deck ships")
            if ship_count_values.count(3) != 2:
                raise Exception("There should be 2 single-deck ships")
            if ship_count_values.count(4) != 1:
                raise Exception("There should be 1 single-deck ship")
        for deck_1, ship_1 in self.field.items():
            for deck_2, ship_2 in self.field.items():
                if ship_1 != ship_2:
                    if (
                            abs(deck_2[0] - deck_1[0]) <= 1
                            and abs(deck_2[1] - deck_1[1]) <= 1
                    ):
                        raise Exception(
                            "Ships shouldn't be located "
                            "in the neighboring cells"
                        )
