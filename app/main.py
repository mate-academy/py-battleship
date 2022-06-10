class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.col = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.is_drowned = is_drowned
        self.decks = []
        self._create_ship(start, end)

    def _create_ship(self, start, end):
        if start[0] == end[0]:
            for column in (range(start[1], end[1] + 1)):
                self.decks.append(Deck(start[0], column))
        else:
            for row in (range(start[0], end[0] + 1)):
                self.decks.append(Deck(start[1], row))

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
            for deck in ship.decks:
                self.field[deck.row, deck.col] = ship
        self._validate_ships_amount()
        self._validate_positions()

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

    def print_field(self):
        field = [
            ["~" for _ in range(10)]
            for _ in range(10)
        ]
        for (row, col), ship in self.field.items():
            if ship.is_drowned:
                field[row][col] = "x"
                continue
            deck = ship.get_deck(row, col)
            field[row][col] = "□" if deck.is_alive else "*"

        column_header = "   ".join([str(num) for num in range(10)])
        print(f"    {column_header}")
        formatted_rows = [
            (f"{num}".center(4, " ") + "   ".join(row))
            for num, row in enumerate(field)
        ]
        print("\n".join(formatted_rows))

    def _validate_positions(self):
        for (row, col), ship in self.field.items():
            for row_delta in range(-1, 2):
                for col_delta in range(-1, 2):
                    check_coords = (row + row_delta, col + col_delta)
                    ship_coords = [
                        (deck.row, deck.col)
                        for deck in ship.decks
                    ]
                    if (check_coords in self.field
                            and check_coords not in ship_coords):
                        raise Exception("Ships shouldn't be located"
                                        "in the neighboring cells")

    def _validate_ships_amount(self):
        ships_amount = {}
        for ship in set(self.field.values()):
            ship_type = len(ship.decks)
            ships_amount[ship_type] = ships_amount.get(ship_type, 0) + 1
        assert sum(ships_amount.values()) == 10, "There no 10 ships on field"
        assert ships_amount[1] == 4, \
            "On field should be four ships with one deck"
        assert ships_amount[2] == 3, \
            "On field should be three ships with two decks"
        assert ships_amount[3] == 2, \
            "On field should be two ships with three decks"
        assert ships_amount[4] == 1, \
            "On field should be one ship with four decks"
