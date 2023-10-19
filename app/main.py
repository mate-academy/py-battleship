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
        self.is_drowned = is_drowned
        if start[0] == end[0] and start[1] == end[1]:
            self.decks = [Deck(start[1], start[0])]
        elif start[0] == end[0]:
            self.decks = [
                Deck(row, start[0])
                for row in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(start[1], column)
                for column in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(location[1], location[0]):
                ship.fire(location[1], location[0])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    field[deck.column][deck.row] = "x"
                elif not deck.is_alive:
                    field[deck.column][deck.row] = "*"
                else:
                    field[deck.column][deck.row] = u"\u25A1"

        for row in field:
            print("  " + "  ".join(row))
        print()
