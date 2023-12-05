class Deck:
    def __init__(
            self,
            row,
            column,
            is_alive=True
    ):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        if start[0] == end[0]:  # Horizontal ship
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:  # Vertical ship
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.check_drowned()

    def check_drowned(self):
        alive_decks = [deck.is_alive for deck in self.decks]
        if not any(alive_decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        self.ships = []
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def _validate_field(self):
        ships_count = len(self.ships)
        single_deck = double_deck = triple_deck = quadruple_deck = 0

        for ship in self.ships:
            decks_count = len(ship.decks)
            if decks_count == 1:
                single_deck += 1
            elif decks_count == 2:
                double_deck += 1
            elif decks_count == 3:
                triple_deck += 1
            elif decks_count == 4:
                quadruple_deck += 1
        if ships_count != 10 or single_deck != 4 or double_deck != 3 or triple_deck != 2 or quadruple_deck != 1:
            raise ValueError("Invalid ships configuration.")

    def fire(self, location):
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
            return "Miss!"
        return "Miss!"

    def print_field(self):
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, col)
                    if not deck.is_alive:
                        print("x", end=" ")  # Drowned ship
                    else:
                        print("*", end=" ")  # Hit deck of the alive ship
                else:
                    print("~", end=" ")  # Empty cell
            print()  # New line for the next row

