class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = [Deck(start[0], start[1])]
        step = end[0] - start[0] + end[1] - start[1]
        for i in range(1, step + 1):
            if end[0] == start[0]:
                self.decks.append(Deck(start[0], start[1] + i))
            else:
                self.decks.append(Deck(start[0] + i, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = True
        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            boat = Ship(ship[0], ship[1])
            self.field[ship[0]] = boat
            step = ship[1][0] - ship[0][0] + ship[1][1] - ship[0][1]
            for i in range(1, step + 1):
                if ship[0][0] == ship[1][0]:
                    self.field[(ship[0][0], ship[0][1] + i)] = boat
                else:
                    self.field[(ship[0][0] + i, ship[0][1])] = boat

    def print_field(self):
        for i in range(10):
            for j in range(10):
                if (i, j) not in self.field:
                    print("~", end="\t")
                elif self.field[(i, j)].is_drowned:
                    print("X", end="\t")
                elif not self.field[(i, j)].get_deck(i, j).is_alive:
                    print("*", end="\t")
                elif (i, j) in self.field:
                    print(u"\u25A1", end="\t")
            print()

    def fire(self, location: tuple):
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
