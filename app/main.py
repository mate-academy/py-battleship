class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            length: int,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = {}
        self.length = length

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks.get((row, column))

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        self.length -= 1
        if self.length == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            start = ship[0]
            end = ship[1]
            ship = Ship(
                start,
                end,
                (end[0] + end[1]) - (start[0] + start[1]) + 1
            )
            for row in range(start[0], end[0] + 1):
                for column in range(start[1], end[1] + 1):
                    self.field[(row, column)] = ship
                    ship.decks[(row, column)] = Deck(row, column)

    def fire(self, location: tuple) -> str:
        if self.field.get(location):
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for coordinates, ship in self.field.items():
            if ship.is_drowned:
                field[coordinates[0]][coordinates[1]] = "x"
            elif ship.get_deck(coordinates[0], coordinates[1]).is_alive:
                field[coordinates[0]][coordinates[1]] = u"\u25A1"
            else:
                field[coordinates[0]][coordinates[1]] = "*"
        for row in field:
            print(row)
