class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks()

    def create_decks(self):
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                deck = Deck(self.start[0], column)
                self.decks.append(deck)
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                deck = Deck(row, self.start[1])
                self.decks.append(deck)
        else:
            deck = Deck(self.start[0], self.start[1])
            self.decks.append(deck)

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        ship_deck = self.get_deck(row, column)
        ship_deck.is_alive = False
        ship_deck_list = [deck.is_alive for deck in self.decks]
        if any(ship_deck_list) is False:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = {}
        self.create_field()
        self.matrix = [["~" for _ in range(10)] for _ in range(10)]

    def create_field(self):
        for coordinates in self.ships:
            ship = Ship(coordinates[0], coordinates[1])
            self.field[tuple(ship.decks)] = ship

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for key, values in self.field.items():
            if values.get_deck(location[0], location[1]):
                values.fire(location[0], location[1])
                if values.is_drowned:
                    for deck in key:
                        self.matrix[deck.row][deck.column] = "x"
                    print("    ".join(self.matrix[deck.row]))
                    return "Sunk!"
                else:
                    self.matrix[location[0]][location[1]] = "*"
                    print("    ".join(self.matrix[location[0]]))
                    return "Hit!"
        return "Miss!"

    def print_field(self):
        for decks in self.field.keys():
            for deck in decks:
                self.matrix[deck.row][deck.column] = u"\u25A1"
        for elem in self.matrix:
            print("    ".join(elem))

    def _validate_field(self):
        numbers_ship = [len(ship) for ship in self.field.keys()]
        if len(numbers_ship) != 10:
            raise Exception("The total number of the ships should be 10")
        if numbers_ship.count(4) != 1:
            raise Exception("There should be 4 single-deck ships")
        if numbers_ship.count(3) != 2:
            raise Exception("There should be 3 double-deck ships")
        if numbers_ship.count(2) != 3:
            raise Exception("There should be 2 three-deck ships")
        if numbers_ship.count(1) != 4:
            raise Exception("There should be 1 four-deck ship")

    def _validate_ship_coordinates(self):
        for coord in self.ships:
            start = coord[0]
            end = coord[1]
            for value in self.field.values():
                if start[0] == end[0]:
                    for column in range(start[1] - 1, end[1] + 2):
                        if value.get_deck(start[0] - 1, column):
                            raise Exception(
                                "ships shouldn't be located "
                                "in the neighboring cells "
                                "(even if cells are neighbors "
                                "by diagonal)"
                            )
                        if value.get_deck(start[0] - 1, column):
                            raise Exception(
                                "ships shouldn't be located "
                                "in the neighboring cells "
                                "(even if cells are neighbors "
                                "by diagonal)"
                            )
                    if value.get_deck(start[0], start[1] - 1):
                        raise Exception(
                            "ships shouldn't be located "
                            "in the neighboring cells "
                            "(even if cells are neighbors "
                            "by diagonal)"
                        )
                    if value.get_deck(end[0], end[1] + 1):
                        raise Exception(
                            "ships shouldn't be located "
                            "in the neighboring cells "
                            "(even if cells are neighbors "
                            "by diagonal)"
                        )
                else:
                    for row in range(start[0] - 1, end[0] + 2):
                        if value.get_deck(row, start[1] - 1):
                            raise Exception(
                                "ships shouldn't be located "
                                "in the neighboring cells "
                                "(even if cells are neighbors "
                                "by diagonal)"
                            )
                        if value.get_deck(row, start[1] + 1):
                            raise Exception(
                                "ships shouldn't be located "
                                "in the neighboring cells "
                                "(even if cells are neighbors "
                                "by diagonal)"
                            )
                    if value.get_deck(start[0] - 1, start[1]):
                        raise Exception(
                            "ships shouldn't be located "
                            "in the neighboring cells "
                            "(even if cells are neighbors "
                            "by diagonal)"
                        )
                    if value.get_deck(end[0] + 1, end[1]):
                        raise Exception(
                            "ships shouldn't be located "
                            "in the neighboring cells "
                            "(even if cells are neighbors "
                            "by diagonal)"
                        )
