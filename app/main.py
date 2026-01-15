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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.hit_decks = []

        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def find_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.find_deck(row, column)

        if deck is None:
            return False

        if deck in self.hit_decks:
            return True

        deck.is_alive = False
        self.hit_decks.append(deck)

        if len(self.hit_decks) == len(self.decks):
            self.is_drowned = True

        return True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}

        for ship_coords in ships:
            ship = Ship(ship_coords[0], ship_coords[1])

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        print("x", end="")
                    elif not deck.is_alive:
                        print("*", end="")
                    else:
                        print(u"\u25A1", end="")
                else:
                    print("~", end="")
            print()

    def validate_field(self) -> None:
        ships = set()
        ship_lengths = []

        for ship in self.field.values():
            if ship not in ships:
                ships.add(ship)
                ship_lengths.append(len(ship.decks))

        if len(ships) != 10:
            raise ValueError("Should be 10 ships!")

        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for length in ship_lengths:
            ship_counts[length] += 1

        if ship_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid ship lengths!")

        for row, column in self.field:
            for delta_row in [-1, 0, 1]:
                for delta_column in [-1, 0, 1]:
                    if delta_row == delta_column == 0:
                        continue
                    neighbor = (row + delta_row, column + delta_column)
                    if ((neighbor in self.field) and self.field[neighbor]
                            != self.field[(row, column)]):
                        raise ValueError("Invalid field!")
