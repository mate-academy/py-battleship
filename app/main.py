class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = []
        for start_row in range(start[0], end[0] + 1):
            for end_cell in range(start[1], end[1] + 1):
                deck = Deck(start_row, end_cell)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:

        deck_in_fire = self.get_deck(row, column)
        if deck_in_fire:
            deck_in_fire.is_alive = False
            if all(not decks.is_alive for decks in self.decks):
                self.is_drowned = True
                return True
        return False


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.ship = Ship(*ship)
            for deck in self.ship.decks:
                self.field[deck.row, deck.column] = self.ship

    def fire(self, location: tuple[int]) -> str:
        if location in self.field:
            ship = self.field[location]
            if ship.fire(location[0], location[1]):
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:

        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        if ship.is_drowned:
                            print("x", end=" ")
                        print("□", end=" ")
                    print("*", end=" ")
                print("~", end=" ")
            print()
