class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False):

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_ship()

    def create_ship(self):
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.end[1]))

        elif self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

        elif self.start[1] == self.end[1]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        self.kill_deck()

    def kill_deck(self):
        for dec in self.decks:
            if dec.is_alive:
                self.is_drowned = False
                break
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list):
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            boat = Ship(ship[0], ship[1])
            for deck in boat.decks:
                self.field[(deck.row, deck.column)] = boat

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
