class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.coordinates = (row, column)
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}) - alive: {self.is_alive} |"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        if start == end:
            self.decks = [Deck(*start)]
        elif start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column
                in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(row, start[1])
                for row
                in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck_fired = self.get_deck(row, column)
        deck_fired.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True

    def __repr__(self) -> str:
        return f"{self.decks}, Drowned: {self.is_drowned} || "


class Battleship:
    def __init__(self, ships: list) -> None:
        ships_list = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in ships_list:
            for deck in ship.decks:
                self.field[deck.coordinates] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if not (row, column) in self.field:
                    print(" ~ ", end="")
                elif self.field[(row, column)].get_deck(row, column).is_alive:
                    print(u" \u25A1 ", end="")
                else:
                    print(" x ", end="")
            print("")
