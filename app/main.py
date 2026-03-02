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

        decks = []
        from_col = min(start[1], end[1])
        to_col = max(start[1], end[1])
        from_row = min(start[0], end[0])
        to_row = max(start[0], end[0])

        if start == end:
            decks.append(Deck(start[0], start[1]))
        elif start[0] == end[0]:
            for i in range(from_col, to_col + 1):
                decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(from_row, to_row + 1):
                decks.append(Deck(i, start[1]))
        self.decks = decks

    def get_deck(self, row, column):
        for i in self.decks:
            if i.row == row and i.column == column:
                return i
        return None

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck:
            if deck.is_alive:
                deck.is_alive = False
            all_dead = True
            for live in self.decks:
                if live.is_alive:
                    all_dead = False
            if all_dead:
                self.is_drowned = True
            else:
                self.is_drowned = False



class Battleship:
    def __init__(self, ships):
        self.ships = [Ship(start, end) for start, end in ships]

    def fire(self, location: tuple):

        for ship in self.ships:
            deck = ship.get_deck(location[0], location[1])
            if deck:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        return "Miss!"

