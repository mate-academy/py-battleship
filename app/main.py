class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        decks = []

        if start == end:
            decks.append(Deck(start[0], start[1]))

        if start[1] != end[1]:
            size = end[1] - start[1]

            for i in range(size + 1):
                decks.append(Deck(start[0], start[1] + i))

        if start[0] != end[0]:
            size = end[0] - start[0]

            for i in range(size + 1):
                decks.append(Deck(start[0] + i, start[1]))

        self.decks = decks

    def hit_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

    def get_fired(self, row, column):
        self.hit_deck(row, column)

        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"

        self.is_drowned = True

        return "Sunk!"

    def get_decks_list(self):
        return [(deck.row, deck.column) for deck in self.decks]


class Battleship:
    def __init__(self, ships):
        self.field = {}
        ship_list = [Ship(*coord) for coord in ships]

        for ship in ship_list:
            for point in ship.get_decks_list():
                self.field[point] = ship

    def fire(self, location: tuple):
        if location not in self.field:
            return "Miss!"

        else:
            ship = self.field[location]

            return ship.get_fired(*location)
