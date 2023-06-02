class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        this_deck = self.get_deck(row, column)
        if this_deck:
            if this_deck.is_alive:
                this_deck.is_alive = False
                self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple[int, int]]) -> None:
        self.field = {
            (row, column): None for column in range(10) for row in range(10)
        }
        for ship in ships:
            current_ship = Ship(*ship)
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship

    def fire(self, location: tuple) -> str:
        if self.field[location]:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field[(row, column)]
                if ship is None:
                    print("~", "\t", end="")
                elif ship.is_drowned:
                    print("x", "\t", end="")
                elif (not ship.is_drowned
                      and ship.get_deck(row, column).is_alive):
                    print("□", "\t", end="")
                else:
                    print("*", "\t", end="")
            print("")
