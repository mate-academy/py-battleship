class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.decks = []
        self.is_drowned = False

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for i in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, i))

        elif c1 == c2:
            for i in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(i, c1))
        else:
            raise ValueError("Ship must be horizontal or vertical")

    def get_deck(self, row: int, column: int) -> set[int]:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if not deck:
            return None

        if not deck.is_alive:
            return "sunk" if self.is_drowned else "hit"

        deck.is_alive = False

        for de in self.decks:
            if de.is_alive:
                self.is_drowned = False
                return "hit"

        self.is_drowned = True
        return "sunk"


class Battleship:
    def __init__(
            self,
            ships: list[
                tuple[
                    tuple[
                        int, int
                    ], tuple[
                        int, int
                    ]
                ]
            ]
    ) -> None:
        self.ships = []
        self.field = {}

        for ship_data in ships:
            ship = Ship(ship_data[0], ship_data[1])
            self.ships.append(ship)

            for deck in ship.decks:
                coord = (deck.row, deck.column)

                if coord in self.field:
                    raise ValueError("Ships overlap")

                self.field[coord] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row, column = location

        result = ship.fire(row, column)

        if result == "hit":
            return "Hit!"
        elif result == "sunk":
            return "Sunk!"

    def print_field(self) -> None:
        for row in range(10):
            row_cells = []

            for col in range(10):
                if (row, col) not in self.field:
                    symbol = "~"
                else:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)

                    if ship.is_drowned:
                        symbol = "x"
                    elif deck.is_alive:
                        symbol = "□"
                    else:
                        symbol = "*"

                row_cells.append(symbol)

            print(" ".join(row_cells))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships")

        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            length = len(ship.decks)

            if length not in counts:
                raise ValueError("Invalid ship length")

            counts[length] += 1

        if counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid fleet composition")

        for (row, col), ship in self.field.items():
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:

                    if dr == 0 and dc == 0:
                        continue

                    nr = row + dr
                    nc = col + dc

                    if 0 <= nr < 10 and 0 <= nc < 10:
                        if (nr, nc) in self.field:
                            neighbor_ship = self.field[(nr, nc)]

                            if neighbor_ship is not ship:
                                raise ValueError("Ships are touching")
