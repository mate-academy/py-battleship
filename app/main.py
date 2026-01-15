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
            is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(start[0], i)
            if start[0] == end[0]
            else Deck(a, 0)
            for a in range(start[0], end[0] + 1)
            for i in range(start[1], end[1] + 1)
        ]
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for i in range(len(self.decks)):
            if self.decks[i].row == row and self.decks[i].column == column:
                return self.decks[i]

    def fire(self, row: int, column: int) -> None:
        for i in self.decks:
            if i == self.get_deck(row, column):
                i.is_alive = False
                self.decks.remove(i)
        if len(self.decks) == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for i in range(len(self.ships)):
            ship = Ship(self.ships[i][0], self.ships[i][1])
            for index in range(len(ship.decks)):
                self.field[ship.decks[index]] = ship

    def fire(self, location: tuple) -> str:
        list_keys = [(keys.row, keys.column) for keys in self.field.keys()]
        if location not in list_keys:
            return "Miss!"

        for keys, value in self.field.items():
            column = keys.column
            row = keys.row

            if row == location[0] and column == location[1]:
                column = keys.column
                row = keys.row
                value.fire(row, column)
                if value.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
