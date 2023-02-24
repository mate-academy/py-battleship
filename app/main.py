class Deck:
    def __init__(self, row, column, is_alive=True):
        self.position = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            if start[1] == end[1]:
                self.decks.append(Deck(start[0], start[1]))
            else:
                for i in range(end[1] - start[1] + 1):
                    self.decks.append(Deck(start[0], start[1] + i))
        else:
            for i in range(end[0] - start[0] + 1):
                self.decks.append(Deck(start[0] + i, start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.position == (row, column):
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck_ in self.decks:
            if deck_.is_alive:
                return
        self.is_drowned = True
        return


class Battleship:

    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            start = ship[0]
            end = ship[1]
            ship_cls = Ship(start, end)
            if start[0] == end[0]:
                if start[1] == end[1]:
                    self.field[start[0], start[1]] = ship_cls
                else:
                    for i in range(end[1] - start[1] + 1):
                        self.field[(start[0], start[1] + i)] = ship_cls
            else:
                for i in range(end[0] - start[0] + 1):
                    self.field[(start[0] + i, start[1])] = ship_cls

    def fire(self, location: tuple):
        try:
            ship = self.field[location]
            for deck in ship.decks:
                if deck.position == location:
                    Ship.fire(ship, location[0], location[1])
                    if ship.is_drowned:
                        return "Sunk!"
                    else:
                        return "Hit!"
        except KeyError:
            return "Miss!"
