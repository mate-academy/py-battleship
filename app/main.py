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
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                deck = Deck(self.start[0], i)
                self.decks.append(deck)
        else:
            for i in range(self.start[0], self.end[0] + 1):
                deck = Deck(i, self.start[1])
                self.decks.append(deck)

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return True

    def fire(self, row, column):
        count_alive = len(self.decks)
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                count_alive -= 1
            else:
                if not deck.is_alive:
                    count_alive -= 1
        if count_alive == 0:
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = dict()
        for i in range(len(ships)):
            start, end = ships[i]
            ship = Ship(start, end)
            if self._validate_field(ship):
                self.field[ships[i]] = ship

    def fire(self, location: tuple):
        row, column = location
        result_fire = False
        for ship_ in self.field:
            if self.field[ship_].get_deck(row, column):
                result_fire = True
                return self.field[ship_].fire(row, column)
        if not result_fire:
            return "Miss!"

    def _validate_field(self, ship):
        len_ship = len(ship.decks)
        valid_len = {4: 1, 3: 2, 2: 3, 1: 4}
        test_len = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship_ in self.field:
            len_ship_ = len(self.field[ship_].decks)
            test_len[len_ship_] += 1
        test_len[len_ship] += 1
        for len_ship_ in test_len:
            if test_len[len_ship_] > valid_len[len_ship_]:
                print(f"Limit is exceeded for {len_ship_} single-deck ships")
                return False
        if len(self.field) > 9:
            print("The limit on the number of ships has been exceeded")
            return False
        for deck in ship.decks:
            around = self.decks_around(deck.row, deck.column)
            for ship_ in self.field:
                for deck_compare in self.field[ship_].decks:
                    if (deck_compare.row, deck_compare.column) in around:
                        print("Ships shouldn't be located "
                              "in the neighboring cells")
                        return False
        return True

    @staticmethod
    def decks_around(x, y):
        up = 0 if x == 9 else 1
        down = 0 if x == 0 else 1
        left = 0 if y == 0 else 1
        right = 0 if y == 9 else 1
        return ((x + up, y - left), (x + up, y), (x + up, y + right),
                (x, y - left), (x, y + right),
                (x - down, y - left), (x - down, y), (x - down, y + right))
