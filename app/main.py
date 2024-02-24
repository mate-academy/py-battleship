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
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(
        self,
        row: int,
        column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
        self,
        row: int,
        column: int
    ) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = not any([cell.is_alive for cell in self.decks])


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        try:
            ship = self.field[location]
            ship .fire(location[0], location[1])
            if ship .is_drowned:
                return "Sunk!"
            return "Hit!"
        except KeyError:
            return "Miss!"

    def print_field(self) -> None:
        new_field = {}
        for row in range(10):
            row_field = {}
            for column in range(10):
                location = (row, column)
                try:
                    if self.field[location].is_drowned:
                        row_field[location] = "x"
                    elif self.field[location].get_deck(row, column).is_alive:
                        row_field[location] = u"\u25A1"
                    else:
                        row_field[location] = "*"
                except KeyError:
                    row_field[location] = "~"
            new_field.update(row_field)

        for row in range(10):
            for column in range(10):
                space = 6 * " "
                print(f"{new_field[(row, column)]}{space}", end="")
            print("\n")
