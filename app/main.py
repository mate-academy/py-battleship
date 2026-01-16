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

    def location(self) -> tuple:
        return self.row, self.column


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        if start[0] == end[0]:
            self.decks = [Deck(start[0], i)
                          for i in range(start[1], end[1] + 1)]
        else:
            self.decks = [Deck(i, start[1])
                          for i in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def location(self) -> list:
        return [deck.location() for deck in self.decks]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if not deck.is_alive:
                self.is_drowned = True
            elif deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    @staticmethod
    def empty_field() -> list:
        return [["\t\t~"] * 10 for _ in range(10)]

    def print_field(self) -> None:
        field = self.empty_field()
        for ship in self.field.values():
            points = ship.location()
            for row, column in points:
                if ship.is_drowned:
                    field[row][column] = "\t\tx"
                elif ship.get_deck(row, column):
                    field[row][column] = "\t\t\u25A1"
                else:
                    field[row][column] = "\t\t*"
        for row in field:
            print("".join(row))
