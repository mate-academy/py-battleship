class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


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
    dict_ships = {}
    field = [["~" for _ in range(10)] for _ in range(10)]

    def __init__(self, ships):
        for ship in ships:
            location_ship = []
            len_ship = abs(sum(ship[0]) - sum(ship[1])) + 1
            if ship[0][0] == ship[1][0]:
                for i in range(len_ship):
                    location_ship.append((ship[0][0], ship[0][1] + i,))
                    self.field[ship[0][0]][ship[0][1] + i] = u"\u25A1"
            else:
                for i in range(len_ship):
                    location_ship.append((ship[0][0] + i, ship[0][1],))
                    self.field[ship[0][0] + i][ship[0][1]] = u"\u25A1"

            self.dict_ships.update({tuple(location_ship): len_ship})

    def print_info(self):
        for column in self.field:
            print(column)

    def fire(self, location: tuple):
        for ship_coordinates in self.dict_ships.keys():
            if location in ship_coordinates:
                self.dict_ships[ship_coordinates] -= 1
                if self.dict_ships[ship_coordinates] <= 0:
                    self.field[location[0]][location[1]] = "x"
                    return "Sunk!"

                self.field[location[0]][location[1]] = "*"
                return "Hit!"
        return "Miss!"
