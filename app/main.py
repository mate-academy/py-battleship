class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.deck = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        self.decks = [(Deck(start[0], start[1]))]
        self.is_drowned = is_drowned
        deck_cords = list(start)
        while tuple(deck_cords) != end:
            if start[1] == end[1]:
                deck_cords[0] += 1
                self.decks.append(Deck(deck_cords[0], deck_cords[1]))
            if start[0] == end[0]:
                deck_cords[1] += 1
                self.decks.append(Deck(deck_cords[0], deck_cords[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.deck == (row, column):
                return deck
        return False

    def fire(self, row: int, column: int):
        if self.get_deck(row, column) is not False:
            self.get_deck(row, column).is_alive = False
            alive_decks = 0
            for deck in self.decks:
                if deck.is_alive is True:
                    alive_decks += 1
            if alive_decks == 0:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships: list):
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(start=ship[0], end=ship[1])

    def fire(self, location: tuple):
        for ship in self.field.keys():
            decks = [ship[0]]
            start = list(ship[0])
            while tuple(start) != ship[1]:
                if ship[0][1] == ship[1][1]:
                    start[0] += 1
                    decks.append((start[0], start[1]))
                if ship[0][0] == ship[1][0]:
                    start[1] += 1
                    decks.append((start[0], start[1]))
            if location in decks:
                return self.field.get(ship).fire(
                    row=location[0],
                    column=location[1])
        return "Miss!"
