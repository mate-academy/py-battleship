class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        pass

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.battle_field = [[0 for _ in range(11)] for _ in range(11)]
        for ship in ships:
            self.battle_field[ship[0][0]][ship[0][1]] = 1
            if ship[0][0] == ship[1][0]:
                for i in range(ship[0][1], ship[1][1] + 1):
                    self.battle_field[ship[0][0]][i] = 1
            else:
                for i in range(ship[0][0], ship[1][0] + 1):
                    self.battle_field[i][ship[0][1]] = 1


    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if self.battle_field[location[0]][location[1]] == 1:
            self.battle_field[location[0]][location[1]] = -1
            if self.battle_field[location[0]][location[1] + 1] != 1 \
                    and self.battle_field[location[0]][location[1] - 1] != 1 \
                    and self.battle_field[location[0] + 1][location[1]] != 1 \
                    and self.battle_field[location[0] - 1][location[1]] != 1:
                return "Sunk!"
            else:
                return "Hit!"

        else:
            return "Miss!"
