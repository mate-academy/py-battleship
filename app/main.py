class Deck:

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other: tuple) -> bool:
        row, column = other
        if self.row == row and self.column == column:
            return True
        return False


class Ship:
    def __init__(
        self,
        start: tuple[int],
        end: tuple[int],
        is_drowned: bool = False
    ) -> None:
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], i) for i in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(i, start[1]) for i in range(start[0], end[0] + 1)
            ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == deck:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple[tuple[int]]) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

    def fire(self, location: tuple[int]) -> str:
        for ship in self.ships:
            if location in ship.decks:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
