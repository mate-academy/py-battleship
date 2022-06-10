class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            [self.decks.append(Deck(start[0], y)) for y in
             range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            [self.decks.append(Deck(x, start[1])) for x in
             range(start[0], end[0] + 1)]

    def get_deck(self, row, column):
        return [self.decks[i] for i, deck in enumerate(self.decks) if
                deck.row == row and deck.column == column][0]

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck is not None:
            if deck.is_alive:
                deck.is_alive = False
                self.is_drowned = True
                for check in self.decks:
                    if check.is_alive:
                        self.is_drowned = False
                        break
                if not self.is_drowned:
                    return "Hit!"
        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship_location in ships:
            ship = Ship(ship_location[0], ship_location[1])
            start, end = ship_location
            if start[0] == end[0]:
                for y in range(start[1], end[1] + 1):
                    self.field[(start[0], y)] = ship
            elif start[1] == end[1]:
                for x in range(start[0], end[0] + 1):
                    self.field[(x, start[1])] = ship

    def fire(self, location: tuple):
        try:
            ship = self.field[location]
        except KeyError:
            return "Miss!"
        row, column = location
        return ship.fire(row, column)

    def print_field(self):
        pass

    def get_coordinates(self, location: tuple):
        try:
            return self.field[location].decks[0]
        except KeyError:
            return None


# sea = Battleship([((2, 0), (2, 3)),
#                   ((4, 5), (4, 6)),
#                   ((3, 8), (3, 9)),
#                   ((6, 0), (8, 0)),
#                   ((6, 4), (6, 6)),
#                   ((6, 8), (6, 9)),
#                   ((9, 9), (9, 9)),
#                   ((9, 5), (9, 5)),
#                   ((9, 3), (9, 3)),
#                   ((9, 7), (9, 7))])
#
# print(sea.get_coordinates((5, 0)))
