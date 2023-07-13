from typing import Union
from tabulate import tabulate


# deck+deck+deck = Ship

class Deck:
    def __init__(self, row, column, is_alive=True):  # PART/COMPONENT
        self.row = row
        self.column = column
        self.is_alive = is_alive

    # def __repr__(self):
    #     return (f"{self.row} | {self.column} | "
    #             f"ALIVE | {self.is_alive} |")
    # def __repr__(self):
    #     return f"({self.row}, {self.column}, {self.is_alive})"
    # def __hash__(self):
    #     # print(hash((self.row, self.column, self.is_alive)))
    #     return hash((self.row, self.column, self.is_alive))


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False
                 ) -> None:  # WHOLE SHIP
        self.decks: [Deck] = []  # Deck/Decks of every Ship

        self.start = start
        self.end = end

        self.is_drowned = is_drowned

        self.direction = None
        self.get_axis()
        self.fill_decks()

    def fill_decks(self):
        if self.start == self.end:
            # self.direction = "single_point"  # □
            self.decks.append(Deck(row=self.start[0], column=self.start[1]))
        if self.start[0] == self.end[0]:
            # self.direction = "x"  # □ □ □
            self.decks = [Deck(row=self.start[0], column=coord) for coord
                          in range(self.start[1], self.end[1] + 1)]
            return
        # self.direction = "y"  # □
        self.decks = [Deck(row=coord, column=self.start[1]) for coord
                      in range(self.start[0], self.end[0] + 1)]
        # self.decks.extend([Deck(row=self.start[0], column=self.start[1])] if self.start == self.end
        #                   else [Deck(row=self.start[0], column=coord) for coord in range(self.start[1], self.end[1] + 1)] if self.start[0] == self.end[0]
        #                   else [Deck(row=coord, column=self.start[1]) for coord in range(self.start[0], self.end[0] + 1)])

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None
        # Find the Deck instance by coords

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        # print(self.decks)
        if deck:
            damaged_decks = 0
            deck.is_alive = False
            # self.decks.remove(deck)  # no need to remove, need to check status
            for i in self.decks:
                if not i.is_alive:
                    damaged_decks += 1
                # print(i)
                # print(i.is_alive)
                # print(type(i))
            if damaged_decks == len(self.decks):
                self.is_drowned = True

    # def __repr__(self):
    #     return f"{self.start}, {self.end}, {self.is_drowned}"

    def get_axis(self):  # custom
        if self.start == self.end:
            self.direction = "single_point"  # □
            return
        if self.start[0] == self.end[0]:
            self.direction = "x"  # □ □ □
            return
        self.direction = "y"  # □
        # ______________________□
        # ______________________□

    def get_neighbors(self, neighboring_cells):
        print("checking neighbors", self.direction)
        counter = len(self.decks)
        ship_neighbors = []
        for deck in self.decks:
            if (deck.row, deck.column) in neighboring_cells:
                return False
            counter -= 1
            print(deck.row, deck.column)
            deck_neighbors = [(deck.row - 1, deck.column - 1),
                              (deck.row - 1, deck.column),
                              (deck.row - 1, deck.column + 1),
                              (deck.row, deck.column - 1),
                              None, (deck.row, deck.column + 1),
                              (deck.row + 1, deck.column - 1),
                              (deck.row + 1, deck.column),
                              (deck.row + 1, deck.column + 1)]

            if self.direction == "single_point":
                ship_neighbors.extend(deck_neighbors)

            if self.direction == "x":
                print("counter: ", counter)
                if counter != 0:
                    deck_neighbors[5] = None
                ship_neighbors.extend(deck_neighbors)

            if self.direction == "y":
                if counter != 0:
                    deck_neighbors[7] = None
                ship_neighbors.extend(deck_neighbors)

        return ship_neighbors
        # if self.direction == "x":
        #     print(deck.row,deck.column)
        #     left, mid, right = (deck.row-1,deck.row,)
        #     neighbors = [(left, left), (left, mid), (left, right),
        #                  (mid, left),                (mid, right),
        #                  (right, left), (right, mid), (right, right)]
        #     counter -= 1
        # if self.direction == "y":
        #     left, mid, right = (0,0,0)
        #     neighbors = [(left, left), (left, mid), (left, right),
        #                  (mid, left),                 (mid, right),
        #                  (right, left), (right, mid), (right, right)]
        print(counter)


class Battleship:
    def __init__(self, ships: list[tuple]):  # Whole game
        self.field = {}  # Create a dict `self.field`. # ((), (), ... ()) : self.Ship
        # counter = 1
        for coord in ships:  # debug
            ship = Ship(start=coord[0], end=coord[1])
            # print(f"Ship # {counter}:\n{ship}\n")  # debug
            # counter += 1  # debug
            for deck in ship.decks:
                # print(deck)
                self.field[deck] = ship
        # print(self.field)
        # self.validate_input()
        # self.print_field()
        # print(self.field)
        # self.print_field()  # TODO: delete
        if self._validate_input():
            self.print_field()

    def fire(self, location: tuple):  # Loop is not needed. Just check:
        print(f"\n\n\nFIRE TO {location} location!")
        # if location in self.field:
        # print(location)
        # deck = Deck(*location)
        # for i in self.field.keys():
        #     if hash(deck) == hash(i):
        #         print("yay")
        #

        for coord, ship in self.field.items():
            point = (coord.row, coord.column)

            if point == location:
                ship.fire(*location)
                if ship.is_drowned is True:

                    print("Sunk!")
                    self.print_field()
                    return "Sunk!"
                else:

                    print("Hit!")
                    self.print_field()
                    return "Hit!"

        print("Miss!")
        self.print_field()
        return "Miss!"
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

    def print_field(self):

        field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = "□"
                else:
                    if ship.is_drowned:
                        field[deck.row][deck.column] = "x"
                    else:
                        field[deck.row][deck.column] = "*"

        print(tabulate(field, tablefmt="grid"))

    def _validate_input(self):  # Extra
        requirements = {"total_number_of_the_ships": 10,
                        "single_deck_counter": 4,
                        "double_deck_counter": 3,
                        "three_deck_ships": 2,
                        "four_deck_ships": 1,
                        "placement_error": False}
        current_session = {key: False for key in requirements}

        neighboring_cells = []

        for unique_ship in set([ship for ship in self.field.values()]):
            current_session["total_number_of_the_ships"] += 1
            print("\nSHIP: ", unique_ship.start, unique_ship.end, unique_ship.direction)
            placement_check = unique_ship.get_neighbors(neighboring_cells)
            if placement_check is False:
                current_session["placement_error"] = True
            neighboring_cells.extend(placement_check)

            for deck in unique_ship.decks:
                coordinates = (deck.row, deck.column)
                neighboring_cells.append(coordinates)

            print(neighboring_cells)

            if len(unique_ship.decks) == 4:
                current_session["four_deck_ships"] += 1
            if len(unique_ship.decks) == 3:
                current_session["three_deck_ships"] += 1
            if len(unique_ship.decks) == 2:
                current_session["double_deck_counter"] += 1
            if len(unique_ship.decks) == 1:
                current_session["single_deck_counter"] += 1

        for requirements, result in current_session.items():
            print(f"{' '.join(str(requirements).split(sep='_')).capitalize()}"
                  f" : {result}")
        print(f"{'*' * 31}")
        if current_session == requirements:
            return True


if __name__ == '__main__':
    print("Enter 'exit' to leave")
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )
    battle_ship.print_field()

    while True:
        user_input = list(input("Coordinates to hit:   "))
        coordinates = []
        for num in user_input:
            if num.isnumeric():
                coordinates.append(int(num))

        battle_ship.fire(tuple(coordinates))
