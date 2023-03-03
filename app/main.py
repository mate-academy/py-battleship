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


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.deck = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                ceil = (row, column)
                self.deck.append(ceil)

    def fire(self, row: int, column: int) -> None:
        deck = Deck(row, column)
        self.deck.remove((row, column))
        if not self.deck:
            self.is_drowned = True
        deck.is_alive = False


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            for ceil in ship.deck:
                self.field[ceil] = ship

    def fire(
            self,
            location: tuple
    ) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
