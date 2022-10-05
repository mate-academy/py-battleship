class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        else:
            if end[0] - start[0] != 0:
                for i in range(start[0], end[0] + 1):
                    self.decks.append(Deck(i, start[1]))
            if end[1] - start[1] != 0:
                for i in range(start[1], end[1] + 1):
                    self.decks.append(Deck(start[0], i))
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships):
        self.field = self.create_ships(ships)

    def fire(self, location: tuple):
        if location in self.field.keys():
            return self.field[location].fire(location[0], location[1])
        else:
            return "Miss!"

    @staticmethod
    def create_ships(ships):
        created_ships = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                created_ships[(deck.row, deck.column)] = new_ship
        return created_ships
