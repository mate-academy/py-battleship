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
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        min_row = min(start[0], end[0])
        max_row = max(start[0], end[0])
        min_column = min(start[1], end[1])
        max_column = max(start[1], end[1])

        is_horizontal = min_row == max_row
        is_vertical = min_column == max_column

        if is_horizontal and is_vertical:
            self.decks.append(Deck(min_row, min_column))
            return

        if is_horizontal:
            for column in range(min_column, max_column + 1):
                self.decks.append(Deck(min_row, column))
        elif is_vertical:
            for row in range(min_row, max_row + 1):
                self.decks.append(Deck(row, min_column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        if self.is_drowned:
            return "Sunk!"

        deck = self.get_deck(row, column)

        if not deck:
            return "Miss!"

        if not deck.is_alive:
            return "Miss!"

        deck.is_alive = False

        if any(rest_deck.is_alive for rest_deck in self.decks):
            return "Hit!"

        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for ship in ships:
            start, end = ship
            ship_obj = Ship(start, end)

            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)

        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = []
            for column in range(10):
                coord = (row, column)

                if coord not in self.field:
                    line.append("~")
                    continue

                ship = self.field[coord]

                if ship.is_drowned:
                    line.append("x")
                    continue

                deck = ship.get_deck(row, column)

                if not deck.is_alive:
                    line.append("*")
                    continue

                line.append("□")

            print("".join(line))
