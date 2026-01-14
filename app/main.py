class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not _.is_alive for _ in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            return result
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = "□"
                else:
                    field[deck.row][deck.column] = "*" if not ship.is_drowned\
                        else "x"

        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Should be 10 ships.")

        ships_count = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            decks_count = len(ship.decks)
            if decks_count in ships_count:
                ships_count[decks_count] += 1

        if ships_count != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid deck count.")

        for ship in self.ships:
            for deck in ship.decks:
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        neighbor = (deck.row
                                    + row_offset, deck.column + col_offset)
                        if (neighbor in self.field
                                and self.field[neighbor] != ship):
                            raise ValueError("Ships should not be placed "
                                             "in neighboring cells.")
