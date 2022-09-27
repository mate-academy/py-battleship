class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):

        self.decks = [Deck(*start)]
        self.is_drowned = is_drowned

        # adding all ship decks to list:
        # horizontal ship location
        if start[0] == end[0]:

            # few-decked ships
            if start[1] != end[1]:
                n_decks_after_start = end[1] - start[1]
                for n in range(1, n_decks_after_start + 1):
                    self.decks.append(Deck(start[0], start[1] + n))

        # vertical ship location
        else:
            n_decks_after_start = end[0] - start[0]
            for n in range(1, n_decks_after_start + 1):
                self.decks.append(Deck(start[0] + n, start[1]))

    def get_deck(self, row, column):
        """
        Returns required deck
        """
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row, column):
        """
        Hits the deck
        """
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {}
        # key is a tuple - decks coords, value is the corresponding ships
        for ship in ships:
            ship_obj = Ship(*ship)
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj
        self._validate_field()

    def fire(self, location: tuple):
        """
        Makes a game move and, if it's lucky, hits or drowns the ship
        """
        is_deck = location in self.field
        if is_deck:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self):
        """
        Prints battlefield cells and their current state
        """
        field_board = [list(["~"] * 10) for _ in range(10)]
        for i in range(10):
            for j in range(10):
                if (i, j) in self.field:

                    deck_tuple = (i, j)
                    ship = self.field[deck_tuple]

                    if ship.is_drowned:
                        field_board[i][j] = "x"
                    else:
                        deck_obj = ship.get_deck(i, j)

                        if deck_obj.is_alive is False:
                            field_board[i][j] = "*"
                        else:
                            field_board[i][j] = "a"

        for i in field_board:
            print(" ".join(i))

    def _validate_field(self):
        """
        Checks whether all conditions for ships quantity and positions
        are satisfied, otherwise - rises error
        """
        # checking the quantity of ships
        assert len(set(self.field.values())) == 10, \
            "The total number of the ships should be 10"

        # checking the quantities of different-type-decked ships
        decks = [len(ship.decks) for ship in set(self.field.values())]

        def check_quantity(num_decks, str_num_decks, quant_expected):
            assert decks.count(num_decks) == quant_expected, \
                f"There should be {quant_expected} {str_num_decks}-deck ships"

        check_quantity(1, "single", 4)
        check_quantity(2, "double", 3)
        check_quantity(3, "three", 2)
        check_quantity(4, "four", 1)

        # checking neighbor cells
        def check_neighbor_cell(curr_ship: Ship, cell_coord: tuple):
            try:
                neighbour_ship = self.field[cell_coord]
            except KeyError:
                return False
            except IndexError:
                pass
            else:
                if neighbour_ship != curr_ship:
                    return True

        for deck in self.field:
            curr_ship = self.field[deck]
            coords_to_check = [
                (deck[0], deck[1] + 1),
                (deck[0] + 1, deck[1]),
                (deck[0] + 1, deck[1] + 1)
            ]
            has_heighbor = any(check_neighbor_cell(curr_ship, coords)
                               for coords in coords_to_check)
            assert not has_heighbor, \
                "Ships shouldn't be located in the neighboring cells"
