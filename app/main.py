from __future__ import annotations
from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.deck = (row, column)
        self.is_alive = is_alive

    def __eq__(self, other: Deck) -> bool:
        return self.deck[0] == other.deck[0] and self.deck[1] == other.deck[1]


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        if start[0] == end[0]:
            self.decks = \
                [Deck(start[0], i) for i in range(start[1], end[1] + 1)]
        if start[1] == end[1]:
            self.decks = \
                [Deck(i, start[1]) for i in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned
        self.hp = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        for index in range(len(self.decks)):
            if self.decks[index] == Deck(row, column):
                return self.decks[index]

    def fire(self, row: int, column: int) -> None:
        target = self.get_deck(row, column)
        if target is not None:
            target.is_alive = False
            self.hp -= 1
        if self.hp == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        self.ship_instance_list = []

        for ship in ships:
            self.ship_instance_list.append(Ship(ship[0], ship[1]))

        for ship in self.ship_instance_list:
            for deck in ship.decks:
                self.field[deck.deck] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].hp >= 1:
                return "Hit!"
            return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        for coord_x in range(0, 10):
            for coord_y in range(0, 10):
                if (coord_x, coord_y) in self.field:
                    if self.field[(coord_x, coord_y)].get_deck(
                            coord_x, coord_y
                    ).is_alive is True:
                        print(u"\u25A1", end="   ")
                    elif (self.field[(coord_x, coord_y)].get_deck(
                            coord_x, coord_y
                    ).is_alive is False) \
                            and (self.field[(coord_x,
                                             coord_y)].is_drowned is False):
                        print("*", end="   ")
                    elif (self.field[(coord_x, coord_y)].get_deck(
                            coord_x, coord_y
                    ).is_alive is False) \
                            and (self.field[(coord_x,
                                             coord_y)].is_drowned is True):
                        print("x", end="   ")
                else:
                    print("~", end="   ")
            print()

    def _validate_field(self) -> None:
        self._validate_number_of_ships()
        self._validate_number_of_decks_per_ship()
        self._validate_neighboring_cells()

    def _validate_number_of_ships(self) -> None:
        if len(self.ship_instance_list) != 10:
            print("Total number of ships should be equal to 10!")

    def _validate_number_of_decks_per_ship(self) -> None:
        single_deck_ships = 0
        double_deck_ships = 0
        three_deck_ships = 0
        four_deck_ship = 0

        for ship in self.ship_instance_list:
            if ship.hp not in (1, 2, 3, 4):
                print("Number of ship's decks should be in range from 1 to 4!")
            elif ship.hp == 1:
                single_deck_ships += 1
            elif ship.hp == 2:
                double_deck_ships += 1
            elif ship.hp == 3:
                three_deck_ships += 1
            elif ship.hp == 4:
                four_deck_ship += 1

        if single_deck_ships != 4:
            print("There should be 4 single-deck ships!")
        if double_deck_ships != 3:
            print("There should be 3 double-deck ships!")
        if three_deck_ships != 2:
            print("There should be 2 three-deck ships!")
        if four_deck_ship != 1:
            print("There should be 1 four-deck ship!")

    def _validate_neighboring_cells(self) -> None:
        for coord_x in range(0, 9):
            for coord_y in range(0, 9):
                if (((coord_x, coord_y) in self.field)
                    and ((coord_x + 1, coord_y) in self.field)
                        and (self.field[coord_x, coord_y] is not
                             self.field[coord_x + 1, coord_y])) \
                    or (((coord_x, coord_y) in self.field)
                        and ((coord_x, coord_y + 1) in self.field)
                        and (self.field[coord_x, coord_y] is not
                             self.field[coord_x, coord_y + 1])) \
                    or (((coord_x, coord_y) in self.field)
                        and ((coord_x + 1, coord_y + 1) in self.field)
                        and (self.field[coord_x, coord_y] is not
                             self.field[coord_x + 1, coord_y + 1])) \
                    or (((coord_x, coord_y) in self.field)
                        and ((coord_x + 1, coord_y - 1) in self.field)
                        and (self.field[coord_x, coord_y] is not
                             self.field[coord_x + 1, coord_y - 1])):
                    print("Ships shouldn't be located "
                          "in the neighboring cells!")
