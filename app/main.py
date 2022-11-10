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
        self.create()

    def create(self):

        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
            return self.decks
        if self.start[0] == self.end[0]:
            for coord in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], coord))
        if self.start[1] == self.end[1]:
            for coord in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(coord, self.start[1]))

        return self.decks

    def get_deck(self, row, column):

        for deck in self.decks:
            if deck.row == row and deck.column == column:

                return deck

    def fire(self, row, column):

        deck = self.get_deck(row, column)
        deck.is_alive = False

        if not any([deck.is_alive for deck in self.decks]):

            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {}

        for ship in self.ships:

            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple):

        if location in self.field.keys():
            for key, value in self.field.items():

                if key[0] == location[0] and key[1] == location[1]:

                    self.field[key].fire(location[0], location[1])
                    if self.field[key].is_drowned:
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"


if __name__ == '__main__':
    pass
