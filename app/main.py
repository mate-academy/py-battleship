from typing import Union

from tabulate import tabulate
import pygame
import os
import subprocess
import platform


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
        self.forbidden_cells = []
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
        total_number_of_the_ships = 0
        single_deck_counter = 0  # 4
        double_deck_counter = 0  # 3
        three_deck_ships = 0  # 2
        four_deck_ships = 0  # 1
        neighboring_cells = []
        placement_error = False

        for ship in set([ship for ship in self.field.values()]):

            total_number_of_the_ships += 1
            unique_ship = ship
            for deck in unique_ship.decks:
                # print(unique_ship.direction)
                coordinates = (deck.row, deck.column)
                if coordinates in neighboring_cells:
                    placement_error = True
                neighboring_cells.append(coordinates)
                neighbors = self.get_neighbors(coordinates, unique_ship.direction)
                neighboring_cells.extend(neighbors)

                # if unique_ship.direction == "y":
                #     neighboring_cells.append(coordinates[0], coordinates[0])
                #
                # if unique_ship.direction == "single_point":
                #     neighboring_cells.append(coordinates[0], coordinates[0])

                neighboring_cells.append(coordinates)
            print(neighboring_cells)

            if len(unique_ship.decks) == 4:
                four_deck_ships += 1
            if len(unique_ship.decks) == 3:
                three_deck_ships += 1
            if len(unique_ship.decks) == 2:
                double_deck_counter += 1
            if len(unique_ship.decks) == 1:
                single_deck_counter += 1

        print(f"The total number of the ships: {total_number_of_the_ships}")
        print(f"Single-deck ships amount: {single_deck_counter}")
        print(f"Double-deck ships amount: {double_deck_counter}")
        print(f"Three-deck ships amount: {three_deck_ships}")
        print(f"Four-deck ships amount: {four_deck_ships}")
        print(f"Neighboring cells filled: {placement_error}")
        # TODO: ships shouldn't be located in the neighboring cells
        # TODO: (even if cells are neighbors by diagonal
        if total_number_of_the_ships == 10:
            if single_deck_counter == 4:
                if double_deck_counter == 3:
                    if three_deck_ships == 2:
                        if four_deck_ships == 1:
                            if not placement_error:
                                print(f"\n{'*' * 17} VALID {'*' * 17}\n")
                                return True

    @staticmethod
    def get_neighbors(coordinates, direction):
        row, column = coordinates
        neighbors = []

        if direction == "x":
            if column - 1 >= 0:
                neighbors.append((row, column - 1))
                if row - 1 >= 0:
                    neighbors.append((row - 1, column - 1))
                if row + 1 < 10:
                    neighbors.append((row + 1, column - 1))
            if row - 1 >= 0:
                neighbors.append((row - 1, column))
            if row + 1 < 10:
                neighbors.append((row + 1, column))
            if column + 1 < 10 and row + 1 < 10:
                neighbors.append((row + 1, column + 1))
            if column - 1 >= 0 and row + 1 < 10:
                neighbors.append((row + 1, column - 1))

        if direction == "y":
            if column - 1 >= 0:
                neighbors.append((row, column - 1))
                if row - 1 >= 0:
                    neighbors.append((row - 1, column - 1))
            if column + 1 < 10:
                neighbors.append((row, column + 1))
                if row - 1 >= 0:
                    neighbors.append((row - 1, column + 1))
            if row - 1 >= 0:
                neighbors.append((row - 1, column))
            if row + 1 < 10:
                neighbors.append((row + 1, column))


        elif direction == "single_point":
            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):
                    if i == row and j == column:
                        continue
                    if 0 <= i < 10 and 0 <= j < 10:
                        neighbors.append((i, j))
        return neighbors


if __name__ == '__main__':
    print("MAIN.PY -> print testing")
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
    # battle_ship.fire((0, 0))
    # battle_ship.fire((0, 1))
    # battle_ship.fire((0, 2))
    # battle_ship.fire((0, 3))
    # battle_ship.fire((0, 6))
    # battle_ship.fire((0, 7))
