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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:
        if self.start[0] == self.end[0]:
            row = self.start[0]
            decks = [
                (Deck(row, column))
                for column in range(self.start[1], self.end[1] + 1)
            ]
        else:
            column = self.start[1]
            decks = [
                (Deck(row, column))
                for row in range(self.start[0], self.end[0] + 1)
            ]

        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None:
        if deck := self.get_deck(row, column):
            deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships_coord = ships
        self.field = self.create_field()

    def create_field(self) -> dict:
        field = {}
        for ship_coord in self.ships_coord:
            ship = Ship(ship_coord[0], ship_coord[1])
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        empty = "~"
        full = u"\u25A1"
        hit_decks = "*"
        drowned_decks = "x"

        for row in range(10):
            for column in range(10):
                coord = (row, column)
                if coord not in self.field:
                    print(empty, end=" ")
                    continue
                ship = self.field[coord]
                if ship.is_drowned:
                    print(drowned_decks, end=" ")
                elif ship.get_deck(row, column).is_alive:
                    print(full, end=" ")
                else:
                    print(hit_decks, end=" ")
            print()
