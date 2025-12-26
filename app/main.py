class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_deck(start, end)

    def get_deck(self, start: tuple, end: tuple) -> list:
        row1, column1 = start
        row2, column2 = end
        deck = []
        if row1 == row2:
            step = 1 if column2 >= column1 else -1
            for column in range(column1, column2 + step, step):
                deck.append(Deck(row1, column))
        elif column1 == column2:
            step = 1 if row2 >= row1 else -1
            for row in range(row1, row2 + step, step):
                deck.append(Deck(row, column1))
        else :
            raise ValueError("Ship must be vertical or horizontal")
        return deck

    def fire(self, row: int, column: int) -> None:
        for i in self.decks:
            if i.row == row and i.column == column:
                if i.is_alive:
                    i.is_alive = False
        for i in self.decks:
            if i.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.WATER = "~"
        self.HIT = "*"
        self.MISS = "0"
        self.SUNK = "x"
        self.SHIP = u"\u25A1"
        self.field = {}
        self.arena = [[self.WATER] * 10 for _ in range(10)]
        for start, end in ships:
            shi = Ship(start, end)
            for i in shi.decks:
                self.field[(i.row, i.column)] = shi
        for row, column in self.field:
            self.arena[row][column] = self.SHIP
        self.print_field()
        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location
        if location in self.field:
            self.field[location].fire(row, column)
            if self.field[location].is_drowned:
                self.print_field()
                return "Sunk!"
            self.arena[row][column] = self.HIT
            self.print_field()
            return "Hit!"
        self.arena[row][column] = self.MISS
        self.print_field()
        return "Miss!"

    def print_field(self) -> None:
        for dec in self.field:
            row, column = dec
            if self.field[dec].is_drowned:
                self.arena[row][column] = self.SUNK
        print("_" * 29)
        for row in range(10):
            print("  ".join(self.arena[row]))

    def _validate_field(self) -> None:
        ships = {ship for ship in self.field.values()}
        occupied = set()
        four_decks = 0
        three_decks = 0
        two_decks = 0
        one_deck = 0
        number_ships = 0
        for deck in ships:
            number_decks = len(deck.decks)
            if number_decks == 4:
                four_decks += 1
                number_ships += 1
            elif number_decks == 3:
                three_decks += 1
                number_ships += 1
            elif number_decks == 2:
                two_decks += 1
                number_ships += 1
            elif number_decks == 1:
                one_deck += 1
                number_ships += 1
            else:
                raise ValueError(f"Incorrect ship length"
                                 f" {deck.start, deck.end}")
        if four_decks != 1:
            raise ValueError("Should be 1 four_decker")
        if three_decks != 2:
            raise ValueError("Should be 2 three_decker")
        if two_decks != 3:
            raise ValueError("Should be 3 two_decker")
        if one_deck != 4:
            raise ValueError("Should be 4 one_decker")
        if number_ships != 10:
            raise ValueError("Should be 10 ships")
        for ship in ships:
            for deck in ship.decks:
                row, column = deck.row, deck.column

                for d_row in [-1, 0, 1]:
                    for d_column in [-1, 0, 1]:
                        if d_row == 0 and d_column == 0:
                            continue
                        new_row, new_column = row + d_row, column + d_column
                        if (new_row, new_column) in occupied:
                            conflict = self.field[(new_row, new_column)]
                            raise ValueError(f"Ship"
                                             f" {ship.start, ship.end} and"
                                             f" {conflict.start, conflict.end}"
                                             f" nearby")
            for deck in ship.decks:
                occupied.add((deck.row, deck.column))
