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
        is_drowned: bool = False,
    ) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(
                min(start[0], end[0]),
                max(start[0], end[0]) + 1,
            )
            for column in range(
                min(start[1], end[1]),
                max(start[1], end[1]) + 1,
            )
            if start[0] == end[0] or start[1] == end[1]
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if any(d.is_alive for d in self.decks):
                return "Hit!"
            self.is_drowned = True
            return "Sunk!"
        return "Miss!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        self.shots = set()
        for ship_data in ships:
            ship = Ship(*ship_data)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.shots:
            self.shots.add(location)
            if location not in self.field:
                return "Miss!"
            return self.field[location].fire(*location)
        return "Already fired!"
