from __future__ import annotations
from app.error import DeckError

import copy


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.coordinates = []
        self.set_coordinates(start, end)

    def fire(self) -> None:
        self.is_drowned = True

    def set_coordinates(self, start: tuple, end: tuple) -> None:
        if start == end:
            self.coordinates = [start]
        elif start[0] == end[0]:
            range_ = range(start[1], end[1] + 1)
            self.coordinates = list((start[0], y) for y in range_)
        elif start[1] == end[1]:
            range_ = range(start[0], end[0] + 1)
            self.coordinates = list((y, start[1]) for y in range_)


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.single_deck = 0
        self.double_deck = 0
        self.triple_deck = 0
        self.four_deck = 0
        self.deck = []
        for column in range(self.column):
            self.deck.append(["~"] * self.row)

    def print_field(self) -> None:
        for row in self.deck:
            print(row)

    def number_of_the_ships(self) -> int:
        single_double = self.single_deck + self.double_deck
        triple_four = self.triple_deck + self.four_deck
        return single_double + triple_four

    def count_multi_decks(self, deck_count: int) -> None:
        if deck_count == 2:
            self.double_deck += 1
        elif deck_count == 3:
            self.triple_deck += 1
        elif deck_count == 4:
            self.four_deck += 1

    def _validate_field(self) -> None:
        if self.number_of_the_ships() != 10:
            raise DeckError("Number of Ships should be equals 10")
        if self.single_deck != 4:
            raise DeckError("Number of single block ships should be equals 4")
        if self.double_deck != 3:
            raise DeckError("Number of double block ships should be equals 3")
        if self.triple_deck != 2:
            raise DeckError("Number of triple block ships should be equals 2")
        if self.four_deck != 1:
            raise DeckError("Number of four block ships should be equals 1")

    def add_deck(self, deck_to_add: Ship) -> None:
        x_coord = deck_to_add.start
        y_coord = deck_to_add.end
        if x_coord == y_coord:
            self.deck[x_coord[0]][x_coord[1]] = "□"
            self.single_deck += 1
        elif x_coord[0] == y_coord[0]:
            deck_count = ["□"] * (y_coord[1] - x_coord[1] + 1)
            self.deck[x_coord[0]][x_coord[1]: y_coord[1] + 1] = deck_count
            self.count_multi_decks(deck_count)
        elif x_coord[1] == y_coord[1]:
            deck_count = abs(x_coord[0] - y_coord[0]) + 1
            for row in range(x_coord[0], y_coord[0] + 1):
                self.deck[row][x_coord[1]] = "□"
            self.count_multi_decks(deck_count)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.battle_field = Deck(10, 10)
        for ship in ships:
            start = ship[0]
            end = ship[1]
            battle_ship = Ship(start, end)
            self.field[ship] = battle_ship
            self.battle_field.add_deck(battle_ship)
        self.coord_base = copy.deepcopy(self.field)

    def fire(self, location: tuple) -> str:
        column, row = location
        if self.battle_field.deck[column][row] == "~":
            return "Miss!"
        if self.battle_field.deck[column][row] == "□":
            self.battle_field.deck[column][row] = "*"
            for ship_ in self.field:
                if location in self.field[ship_].coordinates:
                    self.field[ship_].coordinates.remove(location)
                    self.battle_field.deck[column][row] = "*"
                    if not self.field[ship_].coordinates:
                        for coord in self.coord_base[ship_].coordinates:
                            self.battle_field.deck[coord[0]][coord[1]] = "x"
                        self.field[ship_].fire()
                        return "Sunk!"
                    return "Hit!"
