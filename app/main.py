class Deck:
    battle_field = []

    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.battle_field = [["~" for _ in range(self.row)] for _ in range(self.column)]
        self.is_alive = is_alive


class Ship:

    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row, column):
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
