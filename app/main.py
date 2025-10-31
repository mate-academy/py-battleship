class Deck:
    def __init__(self, row, column, is_alive=True):
        self.is_alive = is_alive
        self.row = row
        self.column = column
        self.coords = (row, column)


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.fire_decks = 0

        self.decks = [Deck(*coords) for coords in self.find_coords()]

    def find_coords(self):
        coords = []

        x1, y1 = self.start
        x2, y2 = self.end

        if y1 == y2:
            step_x = 1 if x1 < x2 else -1

            for x in range(x1, x2 + step_x, step_x):
                coords.append((x, y1))

        elif x1 == x2:
            step_y = 1 if y1 < y2 else -1

            for y in range(y1, y2 + step_y, step_y):
                coords.append((x1, y))

        return coords


    # def get_deck(self, row, column):
    #     # Find the corresponding deck in the list
    #     pass

    def fire(self, deck, is_drowned=None):
        deck.is_alive = False
        self.fire_decks += 1
        if is_drowned:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]):
        self.count = 0
        self.ships_count = {4: 0, 3: 0, 2: 0, 1: 0}
        self.ship_limits = {4: 1, 3: 2, 2: 3, 1: 4}
        self.ships = [Ship(start, end) for start, end in ships if self._validation_field(start, end)]

    def _validation_field(self, start, end):
        if self.count <= 10:
            ship_lenght = end[0] - start[0] + 1 if end[1] == start[1] else end[1] - start[1] + 1

            if ship_lenght in self.ship_limits:
                if self.ships_count[ship_lenght] < self.ship_limits[ship_lenght]:
                    self.ships_count[ship_lenght] += 1
            self.count += 1
            return True
        return False


    def fire(self, location: tuple):
        for ship in self.ships:
            if not ship.is_drowned:

                for deck in ship.decks:
                    if location == deck.coords and deck.is_alive:

                        if ship.fire_decks == len(ship.decks) - 1:
                            ship.fire(deck, is_drowned=True)
                            return "Sunk!"

                        ship.fire(deck)
                        return "Hit!"
        return "Miss!"
