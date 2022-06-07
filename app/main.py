class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.col = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        self.all_ship_coordinates = []
        self._create_ship(start, end)

    def _create_ship(self, start, end):
        coordinates = self._get_all_ship_coordinates(start, end)
        self.all_ship_coordinates = coordinates
        self._create_all_decks(coordinates)
        self.decks = [
            Deck(row_index, col_index)
            for row_index, col_index in coordinates
        ]

    @staticmethod
    def _get_all_ship_coordinates(start, end):
        if start[0] == end[0]:
            columns = list(range(start[1], end[1] + 1))
            rows = [start[0] for _ in range(len(columns))]
        else:
            rows = list(range(start[0], end[0] + 1))
            columns = [start[1] for _ in range(len(rows))]

        return list(zip(rows, columns))

    def _create_all_decks(self, coordinates):
        self.decks = [
            Deck(row_index, col_index)
            for row_index, col_index in coordinates
        ]

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.col:
                return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships):
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for coordinate in ship.all_ship_coordinates:
                self.field[coordinate] = ship

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"
