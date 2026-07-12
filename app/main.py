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
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            row = start[0]
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
        else:
            col = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str | None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

            all_dead = all(not ship_deck.is_alive for ship_deck in self.decks)
            if all_dead:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return None


class Battleship:
    def __init__(self, ships: tuple[int, int]) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.cells = {}

        for ship_cords in ships:
            ship = Ship(ship_cords[0], ship_cords[1])
            self.ships.append(ship)
            for deck in ship.decks:
                self.cells[(deck.row, deck.column)] = (deck, ship)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location

        for ship in self.ships:
            result = ship.fire(row, column)
            if result in ("Hit!", "Sunk!"):
                return result
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.cells:
                    deck, ship = self.cells[(row, col)]
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif not deck.is_alive:
                        print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Must have exactly 10 ships")

        deck_counts = {}
        for ship in self.ships:
            count = len(ship.decks)
            deck_counts[count] = deck_counts.get(count, 0) + 1

        if deck_counts.get(1) != 4:
            raise ValueError("Must have 4 single-deck ships")

        if deck_counts.get(2) != 3:
            raise ValueError("Must have 3 two-deck ships")

        if deck_counts.get(3) != 2:
            raise ValueError("Must have 2 three-deck ships")

        if deck_counts.get(4) != 1:
            raise ValueError("Must have 1 four-deck ships")

        all_decks = {}
        for ship in self.ships:
            for deck in ship.decks:
                all_decks[(deck.row, deck.column)] = ship
        for ship in self.ships:
            for deck in ship.decks:
                for delta_row in (-1, 0, 1):
                    for delta_column in (-1, 0, 1):
                        neighbor = (
                            deck.row
                            + delta_row, deck.column
                            + delta_column)
                        if (
                                neighbor
                                in all_decks
                                and all_decks[neighbor]
                                != ship
                        ):
                            raise ValueError("Ships are too close!")
