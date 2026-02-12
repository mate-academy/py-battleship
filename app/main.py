from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column})"


class Ship:
    def __init__(self, start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:

        self.is_drowned = is_drowned
        self.decks = []

        for coord in (start, end):
            if not all(0 <= i <= 9 for i in coord):
                raise ValueError(f"The coordinates"
                                 f" {coord} are outside the 10x10 box")

        x1, y1 = start
        x2, y2 = end

        if x1 != x2 and y1 != y2:
            raise ValueError("Diagonal ships are prohibited")

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if x1 == x2 and y1 == y2:
            self.decks.append(Deck(x1, y1))
        elif y2 > y1:
            for i in range(y1, y2 + 1):
                self.decks.append(Deck(x1, i))
        elif x2 > x1:
            for i in range(x1, x2 + 1):
                self.decks.append(Deck(i, y1))

    def __repr__(self) -> str:
        return f"List Decks: ({self.decks}), Is_drowned: ({self.is_drowned})"

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find object ship in list ships (decks)
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field = {}
        self._create_ships(ships)
        self._validate_field()

    def _validate_field(self) -> None:
        ships = set(self.field.values())

        if len(ships) != 10:
            raise ValueError("The field must contain exactly 10 ships.")

        lengths = [len(ship.decks) for ship in ships]
        expected = sorted([4, 3, 3, 2, 2, 2, 1, 1, 1, 1])
        if sorted(lengths) != expected:
            raise ValueError("Incorrect composition of ships.")

        occupied = set(self.field.keys())
        for (row, column) in occupied:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == dc == 0:
                        continue
                    if (row + dr, column + dc) in occupied:
                        if (self.field[(row, column)]
                                != self.field.get((row + dr, column + dc))):
                            raise ValueError("Ships cannot"
                                             " touch, even diagonally.")

    def _create_ships(self,
                      ships: list[tuple[tuple[int, int],
                                        tuple[int, int]]]
                      ) -> None:

        for start, end in ships:
            ship_object = Ship(start, end)
            for deck in ship_object.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError(f"Overlapping ships "
                                     f"at ({deck.row}, {deck.column})")
                self.field[(deck.row, deck.column)] = ship_object

    def fire(self, ceil: tuple) -> str:
        if not isinstance(ceil, tuple) or len(ceil) != 2 \
                or not all(isinstance(x, int) and 0 <= x <= 9 for x in ceil):
            raise ValueError("The shot must be "
                             "a tuple of two numbers from 0 to 9.")

        if ceil not in self.field:
            return "Miss!"

        ship_object = self.field[ceil]
        ship_object.fire(*ceil)
        if ship_object.is_drowned:
            return "Sunk!"
        return "Hit!"
