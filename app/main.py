class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Deck at {self.row}, {self.column}"

    def hit(self) -> None:
        # Change the `is_alive` status of the deck
        self.is_alive = False


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.decks = self.create_decks()
        self.is_drowned = False

    def __str__(self) -> str:
        return f"Ship from {self.start} to {self.end}"

    def create_decks(self) -> list[Deck]:
        return [
            Deck(row, column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.hit()
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = self.create_field()

    def create_field(self) -> dict[tuple, Ship]:
        return {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        # Fire at the location
        row, column = location
        if (row, column) in self.field:
            self.field[(row, column)].fire(row, column)
            if self.field[(row, column)].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        # Print the field with the ships
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].is_drowned:
                        print("x", end=" ")
                    else:
                        if (self.field[(row, column)]
                                .get_deck(row, column)
                                .is_alive):
                            print(u"\u25A1", end=" ")
                        else:
                            print("*", end=" ")
                else:
                    print("~", end=" ")
            print()


if __name__ == "__main__":
    # Create a battleship object and fire at some points
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )

    print(
        battle_ship.fire((0, 4)),  # Miss!
        battle_ship.fire((0, 3)),  # Hit!
        battle_ship.fire((0, 2)),  # Hit!
        battle_ship.fire((0, 1)),  # Hit!
        battle_ship.fire((0, 0)),  # Sunk!
        battle_ship.fire((0, 5)),  # Hit!
    )

    battle_ship.print_field()
