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
        self.decks = []
        st = self.start[0]
        fix_pos = self.end[1]
        iter_pos = self.end[0]
        row = True
        if self.start[0] == self.end[0]:
            row = False
            fix_pos = self.end[0]
            iter_pos = self.end[1]
            st = self.start[1]
        for deck in range(st, iter_pos + 1):
            if not row:
                self.decks.append(Deck(fix_pos, deck))
            else:
                self.decks.append(Deck(deck, fix_pos))

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
        ship_status = [cell.is_alive for cell in self.decks]
        if not any(ship_status):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = [[None for _ in range(10)] for _ in range(10)]
        self.ships = [Ship(value[0], value[1]) for value in self.ships]
        for ship in self.ships:
            for cell in ship.decks:
                self.field[cell.row][cell.column] = cell

    def fire(self, location: tuple) -> str:
        field_loc = self.field[location[0]][location[1]]
        if field_loc is None:
            return "Miss!"
        for ship in self.ships:
            if field_loc in ship.decks:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"

    def print_field(self) -> None:
        for index, deck in enumerate(self.field):
            for count, cell in enumerate(deck):
                if cell is None:
                    self.field[index][count] = "~"
        for ship in self.ships:
            if ship.is_drowned:
                for cell in ship.decks:
                    self.field[cell.row][cell.column] = "x"
            else:
                for cell in ship.decks:
                    if cell.is_alive:
                        self.field[cell.row][cell.column] = u"\u25A1"
                    else:
                        self.field[cell.row][cell.column] = "*"
        for row in self.field:
            for column in row:
                space = 6 * " "
                print(f"{column + space}", end="")
            print("\n")
