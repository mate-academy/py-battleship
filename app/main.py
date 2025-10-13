from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []

        sr, sc = start
        er, ec = end

        for v_ in (sr, sc, er, ec):
            if not isinstance(v_, int):
                raise ValueError("Ship coordinates must be integer.")
            if v_ < 0 or v_ > 9:
                raise ValueError(
                    "Coordinates must be within 0..10 (10x10 grid)."
                )

        if sr != er and sc != ec:
            raise ValueError(
                "Diagonal ships are not allowed (only horizontal or vertical)."
            )

        if sr == er:
            row = sr
            c1, c2 = min(sc, ec), max(sc, ec)
            for c_ in range(c1, c2 + 1):
                self.decks.append(Deck(row, c_))
        else:
            col = sc
            r1, r2 = min(sr, er), max(sr, er)
            for r_ in range(r1, r2 + 1):
                self.decks.append(Deck(r_, col))

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.ships = []

        for coords in ships:
            if not (isinstance(coords, tuple) and len(coords) == 2):
                raise ValueError("Each ship must be ((r1, c1), (r2, c2))")
            start, end = coords
            ship = Ship(start, end)
            for deck in ship.decks:
                cell = (deck.row, deck.column)
                if cell in self.field:
                    raise ValueError(
                        f"Overlapping ships detected at cell {cell}."
                    )
                self.field[cell] = ship
            self.ships.append(ship)

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships on a field.")

        sizes = [len(ship.decks) for ship in self.ships]
        if sizes.count(1) != 4:
            raise ValueError("There must be exactly 4 single-deck ships.")
        if sizes.count(2) != 3:
            raise ValueError("There must be exactly 3 double-deck ships.")
        if sizes.count(3) != 2:
            raise ValueError("There must be exactly 2 three-deck ships.")
        if sizes.count(4) != 1:
            raise ValueError("There must be exactly 1 four-deck ship.")

        all_coords = set(self.field.keys())

        for (row, col) in all_coords:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    neighbor = (row + dr, col + dc)
                    if neighbor in all_coords:
                        if self.field[(row, col)] != self.field[neighbor]:
                            raise ValueError(
                                f"Ships at {(row, col)} and "
                                f"{neighbor} are touching!"
                            )

    def fire(self, location: Tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        for deck in ship.decks:
            if (deck.row, deck.column) == location:
                deck.is_alive = False
                break
        if any(deck.is_alive for deck in ship.decks):
            return "Hit!"
        ship.is_drowned = True
        return "Sunk!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                loc = (row, col)
                if loc in self.field:
                    ship = self.field[loc]
                    if ship.is_drowned:
                        print("x ", end="")
                    else:
                        for deck in ship.decks:
                            if loc == (deck.row, deck.column):
                                if deck.is_alive:
                                    print(u"\u25A1 ", end="")
                                else:
                                    print("* ", end="")
                else:
                    print("~ ", end="")
            print("")
