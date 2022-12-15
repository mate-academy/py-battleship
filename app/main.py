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
        self.decks = [Deck(deck[0], deck[1]) for deck in self.create_middle_decks()]
        # Create decks and save them to a list `self.decks`

    def create_middle_decks(self):
        deck_start_x, deck_start_y = self.start
        deck_end_x, deck_end_y = self.end
        decks_list = []
        if self.start == self.end:
            decks_list = [self.start]
        if deck_start_x == deck_end_x:
            if deck_start_y > deck_end_y:
                while deck_start_y >= deck_end_y:
                    decks_list.append((deck_end_x, deck_end_y))
                    deck_end_y += 1
            if deck_start_y < deck_end_y:
                while deck_start_y <= deck_end_y:
                    decks_list.append((deck_start_x, deck_start_y))
                    deck_start_y += 1
        return decks_list



    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships):
        self.ships = ships
        self.field = {key: Ship(key[0], key[1]) for key in ships}
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

battle_ship = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )

print(battle_ship.field[((9, 3), (9, 3))].decks[0].is_alive)
