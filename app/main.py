class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        else:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return

    def fire(self, row: int, column: int) -> None:
        alive_deck = False

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

            if deck.is_alive:
                alive_deck = True

        if alive_deck is False:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = []
        self.field = {}

        for ship in ships:
            start, end = ship
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)

                    if deck.is_alive:
                        print(u"\u25A1", end=" ")
                    elif ship.is_drowned is False:
                        print("*", end=" ")
                    elif ship.is_drowned:
                        print("x", end=" ")

                else:
                    print("~", end=" ")

            print()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("wrong number of ships")

        one_deck = 0
        two_deck = 0
        three_deck = 0
        four_deck = 0

        for ship in self.ships:
            if len(ship.decks) == 1:
                one_deck += 1
            elif len(ship.decks) == 2:
                two_deck += 1
            elif len(ship.decks) == 3:
                three_deck += 1
            elif len(ship.decks) == 4:
                four_deck += 1

        if one_deck != 4:
            raise ValueError("a single ship is not enough")

        if two_deck != 3:
            raise ValueError("a double ship is not enough")

        if three_deck != 2:
            raise ValueError("a triple ship is not enough")

        if four_deck != 1:
            raise ValueError("a four ship is not enough")

        for ship in self.ships:
            for deck in ship.decks:

                for row_offset in (-1, 0, 1):
                    for column_offset in (-1, 0, 1):

                        if row_offset == 0 and column_offset == 0:
                            continue

                        neighbor = (
                            deck.row + row_offset,
                            deck.column + column_offset
                        )

                        if neighbor in self.field:
                            if self.field[neighbor] is not ship:
                                raise ValueError("ships are touching")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]

            row, column = location
            ship.fire(row, column)

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"
