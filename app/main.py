class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []

        len_ship = abs(sum(start) - sum(end)) + 1
        if start[0] == end[0]:
            for i in range(len_ship):
                self.decks.append(Deck(start[0], start[1] + i))
        else:
            for i in range(len_ship):
                self.decks.append(Deck(start[0] + i, start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        self.get_deck(row, column).is_alive = False

        all_decks_is_alive = [deck.is_alive for deck in self.decks]
        if not any(all_decks_is_alive):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for ship in ships:
            reference_to_ship = Ship(ship[0], ship[1])
            len_ship = abs(sum(ship[0]) - sum(ship[1])) + 1
            if ship[0][0] == ship[1][0]:
                for i in range(len_ship):
                    self.field[ship[0][0], ship[0][1] + i] = reference_to_ship
            else:
                for i in range(len_ship):
                    self.field[ship[0][0] + i, ship[0][1]] = reference_to_ship

    def fire(self, location: tuple):
        if location not in self.field.keys():
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned is True:
            return "Sunk!"
        return "Hit!"
