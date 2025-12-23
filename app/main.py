from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            begin: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        if begin == end:
            self.decks = [Deck(*begin)]
        else:
            self.decks = [Deck(*begin), Deck(*end)]
            row_distance = end[0] - begin[0]
            column_distance = end[1] - begin[1]
            row_deck = []
            column_deck = []
            for i in range(1, row_distance):
                row_deck.append(begin[0] + i)
            for i in range(1, column_distance):
                column_deck.append(begin[1] + i)
            if not row_deck:
                row_deck = [begin[0]] * (column_distance - 1)
            if not column_deck:
                column_deck = [begin[1]] * (row_distance - 1)

            for i in range(len(row_deck)):
                self.decks.append(Deck(row_deck[i], column_deck[i]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            ship_dict = {(deck.row, deck.column): ship
                         for deck in ship.decks}
            self.field.update(ship_dict)

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned is False:
            return "Hit!"
        return "Sunk!"

    def print_field(self) -> None:
        rows = [["~"] * 10 for _ in range(10)]
        for location, ship in self.field.items():
            row = location[0]
            column = location[1]
            if ship.is_drowned:
                rows[row][column] = "x"
            elif not ship.get_deck(*location).is_alive:
                rows[row][column] = "*"
            else:
                rows[row][column] = u"\u25A1"
        joined_rows = ["    ".join(row) for row in rows]
        field = "\n".join(joined_rows)
        print(field)
