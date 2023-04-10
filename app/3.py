class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self._create_decks()

    def _create_decks(self):
        if self.start[0] == self.end[0]:
            # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                deck = Deck(self.start[0], col)
                self.decks.append(deck)
        else:
            # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                deck = Deck(row, self.start[1])
                self.decks.append(deck)

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True

class Battleship:
    def __init__(self, ships):
        self.field = [['~' for _ in range(10)] for _ in range(10)]
        self.ships = ships
        self._validate_field()
        for ship in self.ships:
            r1, c1 = ship[0]
            r2, c2 = ship[1]
            if r1 == r2:
                for c in range(c1, c2 + 1):
                    self.field[r1][c] = '□'
            elif c1 == c2:
                for r in range(r1, r2 + 1):
                    self.field[r][c1] = '□'

    def fire(self, cell):
        row, col = cell
        if self.field[row][col] == '~':
            self.field[row][col] = '*'
            return "Miss!"
        elif self.field[row][col] == '□':
            self.field[row][col] = 'x'
            if self._is_ship_sunk(cell):
                return "Sunk!"
            return "Hit!"

    def print_field(self):
        for row in self.field:
            for cell in row:
                if cell == '~':
                    print(cell, end='\t')
                elif cell == '□':
                    print(u"\u25A1", end='\t')
                elif cell == '*':
                    print('*', end='\t')
                else:
                    print('x', end='\t')
            print()

    def _is_ship_sunk(self, cell):
        for ship in self.ships:
            if cell in ship:
                r1, c1 = ship[0]
                r2, c2 = ship[1]
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        if self.field[r][c] == '□':
                            return False
                return True
        return False

    def _validate_field(self):
        num_ships = len(self.ships)
        num_single = sum(1 for s in self.ships if s[0] == s[1])
        num_double = sum(1 for s in self.ships if abs(s[0][0] - s[1][0]) == 1 or abs(s[0][1] - s[1][1]) == 1)
        num_triple = num_ships - num_single - num_double - 1
        num_quadruple = 1
        if num_ships != 10 or num_single != 4 or num_double != 3 or num_triple != 2 or num_quadruple != 1:
            raise ValueError("Invalid ships configuration")
        for i, ship1 in enumerate(self.ships):
            for j, ship2 in enumerate(self.ships):
                if i != j:
                    r1, c1 = ship1[0]
                    r2, c2 = ship1[1]
                    r3, c3 = ship2[0]
                    r4, c4 = ship2[1]
                    for r in range(r1 - 1, r2 + 2):
                        for c in range(c1 - 1, c2 + 2):
                            if r3 - 1 <= r <= r4 + 1 and c3 - 1 <= c <= c4 + 1:
                                raise ValueError("Ships are too close")

