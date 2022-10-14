class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return u"\u25A1" if self.is_alive is True else "*"


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            row, column = start
            self.decks.append(Deck(row, column))
        else:
            rows_sub, columns_sub = end[0] - start[0], end[1] - start[1]
            if rows_sub == 0:
                row, column = start
                for columns in range(column, column + columns_sub + 1):
                    self.decks.append(Deck(row, columns))
            if columns_sub == 0:
                row, column = start
                for rows in range(row, row + rows_sub + 1):
                    self.decks.append(Deck(rows, column))

    def __repr__(self) -> str:
        return f"{self.decks}"

    def get_deck(self, row: int, column: int) -> any:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
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
        self.field = {}
        for ship_coord in ships:
            start, end = ship_coord
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        print(self._validate_field())

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            row, column = location
            return self.field[location].fire(row, column)
        return "Miss!"

    def print_field(self) -> str:
        field = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                 (0, 7), (0, 8), (0, 9), (1, 0), (1, 1), (1, 2), (1, 3),
                 (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 0),
                 (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                 (2, 8), (2, 9), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                 (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 0), (4, 1),
                 (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                 (4, 9), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
                 (5, 6), (5, 7), (5, 8), (5, 9), (6, 0), (6, 1), (6, 2),
                 (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
                 (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
                 (7, 7), (7, 8), (7, 9), (8, 0), (8, 1), (8, 2), (8, 3),
                 (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 0),
                 (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7),
                 (9, 8), (9, 9)]
        output = ""
        num = 0
        for cell in field:
            num += 1
            if cell in self.field:
                row, column = cell
                if self.field[cell].is_drowned:
                    output += "  x"
                else:
                    output += f"  {self.field[cell].get_deck(row, column)}"
            else:
                output += "  ~"
            if num == 10:
                output += "\n"
                num = 0
        return output

    def _collision_check(self, list_of_ships: set) -> str:
        all_decks_coord_list = self.field.keys()
        for ship in list_of_ships:
            next_cells = []
            ship_decks = []
            for deck in ship.decks:
                ship_decks.append((deck.row, deck.column))
                next_cells.append((deck.row - 1, deck.column - 1))
                next_cells.append((deck.row - 1, deck.column))
                next_cells.append((deck.row - 1, deck.column + 1))
                next_cells.append((deck.row, deck.column - 1))
                next_cells.append((deck.row, deck.column + 1))
                next_cells.append((deck.row + 1, deck.column - 1))
                next_cells.append((deck.row + 1, deck.column))
                next_cells.append((deck.row + 1, deck.column + 1))
            only_next_cells = []
            for cell in next_cells:
                if cell not in ship_decks:
                    only_next_cells.append(cell)
            for cell in set(only_next_cells):
                if cell in all_decks_coord_list:
                    return "Stop"

    def _validate_field(self) -> str:
        list_of_ships = set(self.field.values())

        if len(list_of_ships) != 10:
            return "The total number of the ships should be 10"

        check_dict = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in list_of_ships:
            check_dict[len(ship.decks)] += 1
        if check_dict[1] != 4:
            return "There should be 4 single-deck ships"
        if check_dict[2] != 3:
            return "There should be 3 double-deck ships"
        if check_dict[3] != 2:
            return "There should be 2 three-deck ships"
        if check_dict[4] != 1:
            return "There should be 1 four-deck ship"

        if self._collision_check(list_of_ships) == "Stop":
            return "Ships shouldn't be located in the neighboring" \
                   " cells (even if cells are neighbors by diagonal)"

        return "Everything is OK!"
