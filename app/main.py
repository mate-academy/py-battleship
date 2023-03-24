class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = []

        if self.start[0] != self.end[0]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

        if self.start[1] != self.end[1]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = {}

        for ship in ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def __validate_field(self):
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(location[0], location[1])

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"

    def print_field(self):
        field_matrix = []

        for _ in range(10):
            row_items = ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
            field_matrix.append(row_items)

        for location in self.field:
            ship = self.field.get(location)

            if ship.is_drowned:
                field_matrix[location[0]][location[1]] = "X"

            else:
                deck = ship.get_deck(location[0], location[1])

                if deck.is_alive:
                    field_matrix[location[0]][location[1]] = u"\u25A1"
                else:
                    field_matrix[location[0]][location[1]] = "*"

        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in field_matrix]))


battle_ship = Battleship(
    ships=[
        Ship((0, 0), (0, 3)),
        Ship((0, 5), (0, 6)),
        Ship((0, 8), (0, 9)),
        Ship((2, 0), (4, 0)),
        Ship((2, 4), (2, 6)),
        Ship((2, 8), (2, 9)),
        Ship((9, 9), (9, 9)),
        Ship((7, 7), (7, 7)),
        Ship((7, 9), (7, 9)),
        Ship((9, 7), (9, 7)),
    ]
)

print(battle_ship.field)
battle_ship.print_field()

print(battle_ship.fire((0, 4)))  # Miss!
battle_ship.print_field()

print(battle_ship.fire((0, 3)))  # Hit!
battle_ship.print_field()

print(battle_ship.fire((0, 2)))  # Hit!
battle_ship.print_field()

print(battle_ship.fire((0, 1)))  # Hit!
battle_ship.print_field()

print(battle_ship.fire((0, 0)))  # Sunk!
battle_ship.print_field()

