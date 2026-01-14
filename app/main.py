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
        self.decks = self.ships_decks()

    def ships_decks(self) -> list:
        if self.start[0] == self.end[0]:
            return [Deck(self.start[0], i)
                    for i in range(self.start[1], self.end[1] + 1)]
        elif self.start[1] == self.end[1]:
            return [Deck(i, self.start[1])
                    for i in range(self.start[0], self.end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        hit_deck = self.get_deck(row, column)
        if hit_deck:
            hit_deck.is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = self.battle_field()

    def battle_field(self) -> dict:
        field = {}
        ships = [Ship(ship[0], ship[1]) for ship in self.ships]
        for ship in ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        elif not self.field[location].is_drowned:
            return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            row_string = ""
            for column in range(10):
                if (row, column) not in self.field:
                    row_string += "~"
                elif self.field[(row, column)].is_drowned:
                    row_string += "x"
                elif self.field[(row, column)].get_deck(row, column).is_alive:
                    row_string += "="
                elif not (self.field[(row, column)].
                          get_deck(row, column).is_alive):
                    row_string += "*"
            print(row_string)
