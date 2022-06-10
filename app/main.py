class Field:
    def __init__(self, added_ships):
        self.field = []
        for _ in range(10):
            self.field.append(
                [' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ ',
                 ' ~ '
                 ]
            )
        for (start, end) in added_ships.keys():
            self.field[start][end] = " □ "

    def print_field(self):
        for line in self.field:
            print('  '.join(map(str, line)))
        print("\n")

    def fight(self, row: int = None, column: int = None, ship=None):
        if ship is None:
            self.field[row][column] = " * "

        else:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = " x "


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_downed = is_drowned
        self.decks = []
        self.length = 0

        for i in range(start[1], end[1] + 1):
            self.decks.append(Deck(start[0], i))
            self.length += 1

    def get_deck(self, row, column):
        for deck in self.decks:
            if row == deck.row and column == deck.column and deck.is_alive:
                return deck

            if row == deck.row \
                    and column == deck.column \
                    and deck.is_alive is False:
                if self.is_downed:
                    return "Sunk!"

    def fire(self, deck):
        deck.is_alive = False
        self.length -= 1

        if self.length == 0:
            self.is_downed = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    visual_field = None

    def __init__(self, ships):
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for i in range(start[1], end[1] + 1):
                self.field[(start[0], i)] = ship

        self.visual_field = Field(self.field)
        self.visual_field.print_field()

    def fire(self, location: tuple):
        row, column = location

        self.visual_field.fight(row, column)
        self.visual_field.print_field()

        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(row, column)

            if deck == "Sunk!":
                return deck

            if deck.is_alive:
                answer = ship.fire(deck)
                if answer == "Sunk!":
                    self.visual_field.fight(ship=ship)
                    self.visual_field.print_field()
                return answer

        return "Miss!"

battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)
print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)