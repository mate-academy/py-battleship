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
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        if start[0] == end[0] and start[1] == end[1]:
            deck = Deck(start[0], start[1])
            self.decks.append(deck)
        elif start[0] == end[0]:
            for i in range(end[1] - start[1] + 1):
                deck = Deck(start[0], start[1] + i)
                self.decks.append(deck)
        elif start[1] == end[1]:
            for i in range(end[0] - start[0] + 1):
                deck = Deck(start[0] + i, start[1])
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> str | None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        founded_deck = self.get_deck(row, column)
        if founded_deck:
            founded_deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive is False:
                    continue
                else:
                    return "Hit!"
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field.get((row, column))
                if ship:
                    deck_on_cell = ship.get_deck(row, column)
                    if deck_on_cell.is_alive:
                        print(u"\u25A1", end=" ")
                    elif ship.is_drowned:
                        print("*", end=" ")
                    else:
                        print("x", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        unique_ships = set(self.field.values())
        if len(unique_ships) != 10:
            raise ValueError

        count_of_decks = {}
        for unique_ship in unique_ships:
            if not len(unique_ship.decks) in count_of_decks:
                count_of_decks[len(unique_ship.decks)] = 1
            else:
                count_of_decks[len(unique_ship.decks)] += 1

        if count_of_decks != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError

        for (row, col), current_ship in self.field.items():
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue

                    neighbor_coord = (row + dr, col + dc)

                    if neighbor_coord in self.field:
                        neighbor_ship = self.field[neighbor_coord]
                        if neighbor_ship != current_ship:
                            raise ValueError("Ships are located "
                                             "in neighboring cells!")
