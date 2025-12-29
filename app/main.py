class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple, is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        if start == end:
            self.start_column = start[1]
            self.end_column = self.start_column
            self.end_row = end[0]
            self.start_row = self.end_row
            self.decks.append(Deck(self.start_row, self.end_column))
            self.position = "single"
        elif start[0] == end[0]:
            self.position = "horizontal"
            row = start[0]
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
            self.start_column, self.end_column = start[1], end[1]
        elif start[1] == end[1]:
            self.position = "vertical"
            column = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, column))
            self.start_row, self.end_row = start[0], end[0]

    def __str__(self) -> str:
        ship = ""
        if self.position == "single":
            ship += "□"
        if self.position == "horizontal":
            for _ in range(len(self.decks)):
                ship += "□  "

        if self.position == "vertical":
            for _ in range(len(self.decks)):
                ship += "□\n"

        return f"\n{ship}\n"

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for cell in new_ship.decks:
                self.field[(cell.row, cell.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        field_map = {row: ["~"] * 10 for row in range(10)}
        for location, ship in self.field.items():
            row, column = location
            if ship.get_deck(row, column).is_alive:
                field_map[row][column] = "□"
            elif ship.is_drowned:
                field_map[row][column] = "x"
            else:
                field_map[row][column] = "*"
        for row in field_map.values():
            print("       ".join(row))

    # def _validate_field(self) -> None:
    #
    #     created_ships = set(self.field.values())
    #     if len(created_ships) != 10:
    #         raise Exception(
    #             f"Total number of the ships should be 10."
    #             f"You have {len(created_ships)}"
    #         )
    #     len_n_count_of_ships = {}
    #     for ship in created_ships:
    #         len_of_ship = len(ship.decks)
    #         if len_of_ship not in len_n_count_of_ships.keys():
    #             len_n_count_of_ships[len_of_ship] = 1
    #         else:
    #             len_n_count_of_ships[len_of_ship] += 1
    #     for ship_len in len_n_count_of_ships.keys():
    #         if ship_len > 4:
    #             raise Exception(
    #                 "Ships can be only:"
    #                 "   single-deck (len=1)"
    #                 "   double-deck (len=2)"
    #                 "   three-deck (len=3)"
    #                 "   four-deck (len=4)"
    #             )
    #     if (1 not in len_n_count_of_ships.keys()
    #             or len_n_count_of_ships[1] > 4):
    #         count = len_n_count_of_ships[1]\
    #             if 1 in len_n_count_of_ships.keys() else 0
    #         raise Exception(
    #             f"There should be 4 single-deck ships, you have {count}"
    #         )
    #     if (2 not in len_n_count_of_ships.keys()
    #             or len_n_count_of_ships[2] > 3):
    #         count = len_n_count_of_ships[2]\
    #             if 2 in len_n_count_of_ships.keys() else 0
    #         raise Exception(
    #             f"There should be 3 double-deck ships, you have {count}"
    #         )
    #     if (3 not in len_n_count_of_ships.keys()
    #             or len_n_count_of_ships[3] > 2):
    #         count = len_n_count_of_ships[3]\
    #             if 3 in len_n_count_of_ships.keys() else 0
    #         raise Exception(
    #             f"There should be 2 three-deck ships, you have {count}"
    #         )
    #     if (4 not in len_n_count_of_ships.keys()
    #             or len_n_count_of_ships[4] > 1):
    #         count = len_n_count_of_ships[4]\
    #             if 4 in len_n_count_of_ships.keys() else 0
    #         raise Exception(
    #             f"There should be 1 four-deck ships, you have {count}"
    #         )
    #     for ship in created_ships:
    #         if ship.position == "vertical" or ship.position == "single":
    #             column_location = ship.decks[0].column
    #             if ship.start_row in range(1, 9):
    #                 start_row = ship.start_row - 1
    #             else:
    #                 start_row = ship.start_row
    #             if ship.end_row in range(1, 9):
    #                 end_row = ship.end_row + 1
    #             else:
    #                 end_row = ship.end_row
    #             try:
    #                 if column_location in range(1, 10):
    #                     left_column = column_location - 1
    #                     for row in range(start_row, end_row + 1):
    #                         if (row, left_column) in self.field.keys():
    #                             raise Exception
    #                 if column_location in range(0, 9):
    #                     right_column = column_location + 1
    #                     for row in range(start_row, end_row + 1):
    #                         if (row, right_column) in self.field.keys():
    #                             raise Exception
    #                 if (
    #                         start_row != ship.start_row
    #                         and (start_row, column_location)
    #                         in self.field.keys()
    #                         or end_row != ship.end_row
    #                         and (end_row, column_location)
    #                         in self.field.keys()
    #                 ):
    #                     raise Exception
    #             except Exception:
    #                 raise Exception(
    #                     "Ships shouldn't be located in the neighboring cells"
    #                 )
    #     for ship in created_ships:
    #         if ship.position == "horizontal" or ship.position == "single":
    #             row_location = ship.decks[0].row
    #             if ship.start_column in range(1, 9):
    #                 start_column = ship.start_column - 1
    #             else:
    #                 start_column = ship.start_column
    #             if ship.end_column in range(1, 9):
    #                 end_column = ship.end_column + 1
    #             else:
    #                 end_column = ship.end_column
    #             try:
    #                 if row_location in range(1, 10):
    #                     over_row = row_location - 1
    #                     for column in range(start_column, end_column + 1):
    #                         if (over_row, column) in self.field.keys():
    #                             raise Exception
    #                 if row_location in range(0, 9):
    #                     under_row = row_location + 1
    #                     for column in range(start_column, end_column + 1):
    #                         if (under_row, column) in self.field.keys():
    #                             raise Exception
    #                 if (
    #                         start_column != ship.start_column
    #                         and (row_location, start_column)
    #                         in self.field.keys()
    #                         or end_column != ship.end_column
    #                         and (row_location, end_column)
    #                         in self.field.keys()
    #                 ):
    #                     raise Exception
    #             except Exception:
    #                 raise Exception(
    #                     "Ships shouldn't be located in the neighboring cells"
    #                 )
