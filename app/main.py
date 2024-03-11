class GameRules:
    def __init__(self) -> None:
        self.ship_num = 10
        self.ships_amount = {1: 4, 2: 3, 3: 2, 4: 1}


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.location = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        x_coords = [x for x in range(start[0], end[0] + 1)]
        y_coords = [y for y in range(start[1], end[1] + 1)]
        self.decks = [Deck(x, y) for x in x_coords for y in y_coords]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.location == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {
            deck.location: ship for ship in self.ships for deck in ship.decks
        }
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"
        else:
            return "Miss!"

    def _validate_field(self) -> None:
        rules = GameRules()

        if len(self.ships) != rules.ship_num:
            raise Exception(f"Number of ships should be {rules.ship_num}")

        ship_sizes = [len(ship.decks) for ship in self.ships]
        for size, num in rules.ships_amount.items():
            if ship_sizes.count(size) != num:
                raise Exception(f"Number of {size}-deck ships should be {num}")

        neighboring_cells = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for ship in self.ships:
            empty = []
            for deck in ship.decks:
                cell = deck.location
                for point in neighboring_cells:
                    empty.append((cell[0] + point[0], cell[1] + point[1]))
            for item in empty:
                if item in self.field and self.field[item] != ship:
                    raise Exception(
                        "Ships cannot be located in neighboring cells"
                    )
