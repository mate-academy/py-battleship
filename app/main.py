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
            is_drowned : bool = False
    ) -> None:
        if start[0] != end[0]:
            self.decks = [
                Deck(start[0] + i, start[1])
                for i in range(abs(end[0] - start[0]) + 1)
            ]
        elif start[1] != end[1]:
            self.decks = [
                Deck(start[0], start[1] + i)
                for i in range(abs(end[1] - start[1]) + 1)
            ]
        else:
            self.decks = [Deck(start[0], start[1])]

        self.hp = len(self.decks)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> int:
        for i, deck in enumerate(self.decks):
            if deck.row == row and deck.column == column:
                return i

    def fire(self, row: int, column: int) -> str:
        deck_index = self.get_deck(row, column)
        self.decks[deck_index].is_alive = False
        self.hp -= 1
        if self.hp < 1:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship_reference = Ship(ship[0], ship[1])
            for deck in ship_reference.decks:
                self.field[(deck.row, deck.column)] = ship_reference

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field = ""
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        field += "x"
                    elif ship.decks[ship.get_deck(row, column)].is_alive:
                        field += u"\u25A1"
                    else:
                        field += "*"
                else:
                    field += "~"
            field += "\n"

        print(field)
