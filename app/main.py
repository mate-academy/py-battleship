class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: list,
        end: list,
        is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks: list[Deck] = []
        self.is_drowned = is_drowned
        # One-deck ship
        if start == end:
            self.decks = [Deck(*start)]
        else:
            start_row = start[0]
            start_column = start[1]
            end_row = end[0]
            end_column = end[1]
            self.decks = [
                Deck(row, column)
                for row in range(start_row, end_row + 1)
                for column in range(start_column, end_column + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)
        if self.is_drowned:
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field: dict[tuple, Ship] = {}
        for ship in ships:
            present_points = []
            start = ship[0]
            end = ship[1]
            if start[0] != end[0]:
                present_points = [
                    (x, end[1])
                    for x in range(start[0], end[0] + 1)
                ]
            elif start[1] != end[1]:
                present_points = [
                    (start[0], y)
                    for y in range(start[1], end[1] + 1)
                ]
            else:
                present_points = [(ship[0])]
            self.field[tuple(present_points)] = Ship(ship[0], ship[1])
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship_coords in self.field:
            if location in ship_coords:
                return self.field[ship_coords].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        max_column = 9
        max_row = 9
        column = 0
        row = 0
        while column <= max_column:
            while row <= max_row:
                point = row, column
                for i in self.field:
                    if point in i:
                        if self.field[i].is_drowned:
                            print("X", end="")
                        elif self.field[i].get_deck(row, column).is_alive:
                            print("□", end="")
                        else:
                            print("*", end="")
                        break
                    else:
                        print("~", end="")
                row += 1
            print()
            column += 1
            row = 0

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValueError("The total amount of ships should be 10!")
        deck_control = [0, 0, 0, 0]
        for ship in self.field:
            if len(ship) == 4:
                deck_control[3] += 1
            elif len(ship) == 3:
                deck_control[2] += 1
            elif len(ship) == 2:
                deck_control[1] += 1
            elif len(ship) == 1:
                deck_control[0] += 1
        if not (
            deck_control[0] == 4
            and deck_control[1] == 3
            and deck_control[2] == 2
            and deck_control[3] == 1
        ):
            raise ValueError("Incorrect amount of ships was provided!")
        for ship_key in self.field:
            ship_cells = set(ship_key)

            forbidden = set()
            for row, col in ship_cells:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        forbidden.add((row + dr, col + dc))

            for other_key in self.field:
                if other_key == ship_key:
                    continue
                for cell in other_key:
                    if cell in forbidden:
                        raise ValueError("Ships are too close!")
