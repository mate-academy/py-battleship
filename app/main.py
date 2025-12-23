class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.place_deck = (row, column)


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            for i in range(start[1], start[1] + end[1] - start[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            if start[1] == end[1]:
                for i in range(start[0], start[0] + end[0] - start[0] + 1):
                    self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | int:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.place_deck == (row, column):
                return deck
        return 0

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck_shot = self.get_deck(row, column)
        if deck_shot == 0:
            return "Miss!"
        deck_shot.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = {}
        for unit in ships:
            new_ship = Ship(unit[0], unit[1])
            for deck in new_ship.decks:
                self.ships.update({deck.place_deck: new_ship})

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.ships.keys():
            return self.ships[location].fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_string = ""
            for column in range(10):
                if (row, column) in self.ships.keys():
                    row_string += "□	"
                else:
                    row_string += "~	"
            print(row_string)

    def _validate_field(self) -> str:
        ships = {}
        for cell in self.ships.keys():
            if ((cell[0] - 1, cell[1] - 1) in self.ships
                    or (cell[0] + 1, cell[1] - 1) in self.ships
                    or (cell[0] + 1, cell[1] + 1) in self.ships
                    or (cell[0] + 1, cell[1] - 1) in self.ships):
                return "Incorrect location of ships!"
            if ((cell[0], cell[1] - 1) in self.ships
                    and self.ships[(cell[0], cell[1] - 1)]
                    != self.ships[cell]):
                return "Incorrect location of ships!"
            if ((cell[0] + 1, cell[1]) in self.ships
                    and self.ships[(cell[0] + 1, cell[1])]
                    != self.ships[cell]):
                return "Incorrect location of ships!"
            if ((cell[0], cell[1] + 1) in self.ships
                    and self.ships[(cell[0], cell[1] + 1)]
                    != self.ships[cell]):
                return "Incorrect location of ships!"
            if ((cell[0] - 1, cell[1]) in self.ships
                    and self.ships[(cell[0] - 1, cell[1])]
                    != self.ships[cell]):
                return "Incorrect location of ships!"

            ship_lengh = len(self.ships[cell].decks)
            if ship_lengh in ships.keys():
                ships[ship_lengh] += 1
            else:
                ships.update({ship_lengh: 1})

        if {4: 4, 3: 6, 2: 6, 1: 4} != ships:
            return "Wrong quantity of ships!"
        return "Good"
