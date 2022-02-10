class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self):
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        elif self.start[1] == self.end[1]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row: int, column: int):
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int):
        deck_under_fire = self.get_deck(row, column)
        deck_under_fire.is_alive = False
        if True not in [deck.is_alive for deck in self.decks]:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list):
        self.ships = ships
        self.field = {}
        self.adding_decks_to_field()

    def adding_decks_to_field(self):
        for ship_coordinates in self.ships:
            start, end = ship_coordinates
            temp_ship = Ship(start=start, end=end)
            if start[0] == end[0]:
                for i in range(start[1], end[1] + 1):
                    self.field[(start[0], i)] = temp_ship
            if start[1] == end[1]:
                for i in range(start[0], end[0] + 1):
                    self.field[(i, start[1])] = temp_ship

    def fire(self, location: tuple):
        if location in self.field:
            ship_under_fire = self.field[location]
            ship_under_fire.fire(row=location[0], column=location[1])
            if ship_under_fire.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
