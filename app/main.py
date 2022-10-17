class CustomError(Exception):
    pass


class ShipCountError(CustomError):
    pass


class CollisionError(CustomError):
    pass


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
        self._validate_field()

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
        field = [(row, column) for row in range(0, 10)
                 for column in range(0, 10)]
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
                next_cells = [(deck.row + row, deck.column + column)
                              for row in range(-1, 2)
                              for column in range(-1, 2)]
            only_next_cells = []
            for cell in next_cells:
                if cell not in ship_decks:
                    only_next_cells.append(cell)
            for cell in set(only_next_cells):
                if cell in all_decks_coord_list:
                    return "Stop"

    def _validate_field(self) -> None:
        list_of_ships = set(self.field.values())

        # Check total number of the ships
        if len(list_of_ships) != 10:
            raise ShipCountError("The total number of the ships should be 10")

        # Check count of each type of ships
        check_dict = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in list_of_ships:
            check_dict[len(ship.decks)] += 1
        num = 4
        for i in range(1, len(check_dict) + 1):
            if check_dict[i] != num:
                raise ShipCountError(f"There should be {num}"
                                     f" ship(s) with {i} deck ")
            num -= 1

        # Collision check
        if self._collision_check(list_of_ships) == "Stop":
            raise CollisionError("Ships shouldn't be located in the"
                                 " neighboring cells (even if cells"
                                 " are neighbors by diagonal)")
