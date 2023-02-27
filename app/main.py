class Deck:
    def __init__(self, row: int, column: int, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        # print(start)
        # print(end)
        # n = 0 if start[1] == end[1] else 1
        # print(n)
        if start[1] == end[1]:

            for pos in range(start[0], end[0] + 1):
                self.decks.append(Deck(pos, start[1]))
        elif start[0] == end[0]:
            for pos in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], pos))

    def get_deck(self, row, column) -> Deck:
        return [deck for deck in self.decks if deck.row == row and deck.column == column][0]

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if sum([1 for deck_ in self.decks if not deck_.is_alive]) == len(self.decks):
            self.is_drowned = True


class Battleship:
    SHIP_DECK = '□'
    HIT_SHIP_DECK = '*'
    DESTROYED_SHIP_DECK = 'x'
    EMPTY_CELL = '~'

    def __init__(self, ships: list[Ship]) -> None:
        self.field = [[self.EMPTY_CELL for _ in range(10)] for _ in range(10)]
        self.ships = []
        # self._ships_left = 0
        for start, end in ships:
            self._add_ship(start, end)

    def _validate_field(self):
        if not (len(self.ships) == 10):
            raise ValueError
        single = 0
        double = 0
        three = 0
        four = 0
        for ship in self.ships:
            if len(ship.decks) == 1:
                single += 1
            elif len(ship.decks) == 2:
                double += 1
            elif len(ship.decks) == 3:
                three += 1
            elif len(ship.decks) == 4:
                four += 1
        if single != 4 or double != 3 or three != 2 or four != 1:
            raise ValueError

        for ship in self.ships:
            gor = True
            if ship.start[0] == ship.end[0]:
                gor = False
            for i, j in ship.decks:
                if gor and i == 0:
                    if j == 0:
                        if not (self.field[1][0] == self.EMPTY_CELL and self.field[1][1] == self.EMPTY_CELL):
                            raise ValueError
                    elif j == 9:
                        if not (self.field[1][9] == self.EMPTY_CELL and self.field[1][8] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[1][j-1] == self.EMPTY_CELL
                                and self.field[1][j] == self.EMPTY_CELL
                                and self.field[1][j+1] == self.EMPTY_CELL):

                            raise ValueError

                elif gor and i == 9:
                    if j == 0:
                        if not (self.field[8][0] == self.EMPTY_CELL and self.field[8][1] == self.EMPTY_CELL):
                            raise ValueError
                    elif j == 9:
                        if not (self.field[8][9] == self.EMPTY_CELL and self.field[8][8] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[8][j-1] == self.EMPTY_CELL
                                and self.field[8][j] == self.EMPTY_CELL
                                and self.field[8][j+1] == self.EMPTY_CELL):

                            raise ValueError

                else:
                    if j == 0:
                        if not (self.field[i+1][0] == self.EMPTY_CELL
                                and self.field[i+1][1] == self.EMPTY_CELL
                                and self.field[i-1][0] == self.EMPTY_CELL
                                and self.field[i-1][1] == self.EMPTY_CELL):
                            raise ValueError
                    elif j == 9:
                        if not (self.field[i+1][9] == self.EMPTY_CELL
                                and self.field[i+1][8] == self.EMPTY_CELL
                                and self.field[i-1][9] == self.EMPTY_CELL
                                and self.field[i-1][8] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[i+1][j - 1] == self.EMPTY_CELL
                                and self.field[i+1][j] == self.EMPTY_CELL
                                and self.field[i+1][j + 1] == self.EMPTY_CELL
                                and self.field[i-1][j - 1] == self.EMPTY_CELL
                                and self.field[i-1][j] == self.EMPTY_CELL
                                and self.field[i-1][j + 1] == self.EMPTY_CELL):
                            raise ValueError
                if not gor and j == 0:
                    if i == 0:
                        if not (self.field[0][1] == self.EMPTY_CELL and self.field[1][1] == self.EMPTY_CELL):
                            raise ValueError
                    elif i == 9:
                        if not (self.field[9][1] == self.EMPTY_CELL and self.field[8][1] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[i-1][1] == self.EMPTY_CELL
                                and self.field[i][1] == self.EMPTY_CELL
                                and self.field[i+1][1] == self.EMPTY_CELL):
                            raise ValueError

                elif not gor and j == 9:
                    if i == 0:
                        if not (self.field[0][8] == self.EMPTY_CELL and self.field[1][8] == self.EMPTY_CELL):
                            raise ValueError
                    elif i == 9:
                        if not (self.field[9][8] == self.EMPTY_CELL and self.field[8][8] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[i-1][8] == self.EMPTY_CELL
                                and self.field[i][8] == self.EMPTY_CELL
                                and self.field[i+1][8] == self.EMPTY_CELL):
                            raise ValueError

                else:
                    if i == 0:
                        if not (self.field[0][j+1] == self.EMPTY_CELL
                                and self.field[1][j+1] == self.EMPTY_CELL
                                and self.field[0][j-1] == self.EMPTY_CELL
                                and self.field[1][j-1] == self.EMPTY_CELL):
                            raise ValueError
                    elif i == 9:
                        if not (self.field[9][j+1] == self.EMPTY_CELL
                                and self.field[8][j+1] == self.EMPTY_CELL
                                and self.field[9][j-1] == self.EMPTY_CELL
                                and self.field[8][j-1] == self.EMPTY_CELL):
                            raise ValueError

                    else:
                        if not (self.field[i - 1][j + 1] == self.EMPTY_CELL
                                and self.field[i][j+1] == self.EMPTY_CELL
                                and self.field[i + 1][j + 1] == self.EMPTY_CELL
                                and self.field[i - 1][j - 1] == self.EMPTY_CELL
                                and self.field[i][j - 1] == self.EMPTY_CELL
                                and self.field[i + 1][j - 1] == self.EMPTY_CELL):
                            raise ValueError



    # def _add_ship(self, start: tuple, end: tuple) -> None:
    #     self.ships.append(Ship(start, end))
    #     n = 0 if start[1] == end[1] else 1
    #     for pos in range(start[n % 2], end[n % 2] + 1):
    #         self.field[start[(n+1) % 2]][pos] = self.SHIP_DECK

    def print_field(self) -> None:
        for row in self.field:
            for item in row:
                print(item, end=" ")
            print()

    def _add_ship(self, start: tuple, end: tuple) -> None:
        ship = Ship(start, end)
        self.ships.append(ship)
        for deck in ship.decks:
            # if self.field[deck.row][deck.column] == self.EMPTY_CELL:
            self.field[deck.row][deck.column]=self.SHIP_DECK
            # else:
            #     raise ValueError


    def _get_ship(self, row, column) -> Ship:
        for ship in self.ships:
            # if ship.start[0] == ship.end[0]:
            #     if row == ship.start[0] and ship.start[1]<=column<=ship.end[1]:
            #         return ship
            # else:
            #     if row == ship.start[1] and ship.start[0]<=column<=ship.end[0]:
            #         return ship
            n = 0 if ship.start[1] == ship.end[1] else 1
            if row == ship.start[(n+1) % 2] and ship.start[n%2] <= column <= ship.end[n%2]:
                return ship

    def fire(self, location: tuple) -> str:
        x, y = location
        if not (0 <= x <= 9 and 0 <= y <= 9):
            raise ValueError

        # if self.field[x][y] == self.DESTROYED_SHIP_DECK:
        #     return "Sunk!"

        if self.field[x][y] == self.EMPTY_CELL:
            # print(x, y)
            # print("Miss")
            # self.field[x][y] = self.DESTROYED_SHIP_DECK
            return "Miss!"

        ship = self._get_ship(x,y)
        ship.fire(x,y)
        if not ship.is_drowned:
            self.field[x][y]=self.HIT_SHIP_DECK
            # print("Hit")
            return "Hit!"
        else:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = self.DESTROYED_SHIP_DECK
            # print("Sunk!")
            return "Sunk!"
