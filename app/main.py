class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        # Create decks and save them to a list `self.decks`
        if start[0] == end[0]:  # horizontal ship
            row = start[0]
            for column in range(min(start[1], end[1]),
                                max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, column))
        elif start[1] == end[1]:  # vertical ship
            column = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if (deck.row == row and deck.column == column) and deck.is_alive:
                deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = []
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError("Ships shouldn't overlap")
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of ships should be 10")

        count_single_deck = 0
        count_double_decks = 0
        count_three_decks = 0
        count_four_decks = 0
        for ship in self.ships:
            if ship.start == ship.end:
                count_single_deck += 1
            if (abs(ship.start[0] - ship.end[0]) == 1
                    or abs(ship.start[1] - ship.end[1]) == 1):
                count_double_decks += 1
            if (abs(ship.start[0] - ship.end[0]) == 2
                    or abs(ship.start[1] - ship.end[1]) == 2):
                count_three_decks += 1
            if (abs(ship.start[0] - ship.end[0]) == 3
                    or abs(ship.start[1] - ship.end[1]) == 3):
                count_four_decks += 1
        if count_single_deck != 4:
            raise ValueError("There should be 4 single-deck ships")
        if count_double_decks != 3:
            raise ValueError("There should be 3 double-decks ships")
        if count_three_decks != 2:
            raise ValueError("There should be 2 three-decks ships")
        if count_four_decks != 1:
            raise ValueError("There should be 1 four-decks ship ")

        all_decks = []
        for index_ship, ship in enumerate(self.ships):
            for deck in ship.decks:
                all_decks.append((index_ship, deck.row, deck.column))
        for deck in all_decks:
            for deck1 in all_decks:
                if deck[0] == deck1[0]:
                    continue
                if abs(deck[1] - deck1[1]) < 2 and abs(deck[2] - deck1[2]) < 2:
                    raise ValueError("Ships shouldn't be located"
                                     " in the neighboring cells")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            deck.is_alive = False

            ship.is_drowned = all(not deck.is_alive for deck in ship.decks)

            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        matrix = [["~" for _ in range(10)] for _ in range(10)]
        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)

            if deck.is_alive:
                matrix[row][column] = u"\u25A1"
            elif not deck.is_alive and not ship.is_drowned:
                matrix[row][column] = "*"
            elif not deck.is_alive and ship.is_drowned:
                matrix[row][column] = "x"

        for row in matrix:
            print(" ".join(row))
