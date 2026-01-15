

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

    def __repr__(self) -> str:
        return f"row {self.row} column {self.column} is_alive {self.is_alive}"


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if start == end:
            self.decks = [Deck(self.end[0], self.end[1])]
        elif self.start[0] == self.end[0]:
            ship_ = [min(start[1], end[1]), max(start[1], end[1])]
            self.decks = []
            for i in range(ship_[0], ship_[1] + 1):
                self.decks.append(Deck(end[0], i))
        else:
            ship_ = [min(start[0], end[0]), max(start[0], end[0])]
            self.decks = []
            for i in range(ship_[0], ship_[1] + 1):
                self.decks.append(Deck(i, self.end[1]))

    def __repr__(self) -> str:
        return f"start: {self.start} end: {self.end}\n"

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = not deck.is_alive
        if all([not check.is_alive for check in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship_ in ships:
            self.field[ship_] = Ship(ship_[0], ship_[1])

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            deck = ship.get_deck(*location)
            if deck:
                ship.fire(*location)
                print(ship.decks)
                print(ship.is_drowned)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
