from __future__ import annotations

from typing import Tuple


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def __repr__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"

    def create_decks(self) -> list[Deck]:
        list_decks = []
        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                deck = Deck(row=row, column=column)
                list_decks.append(deck)
        return list_decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        fire_deck = self.get_deck(row=row, column=column)
        if fire_deck:
            fire_deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list[Tuple[Tuple[int, int], Tuple[int, int]]]
                 ) -> None:
        self.ships = ships
        self.field = {}
        self.create_field()
        self._validate_field()

    def __repr__(self) -> str:
        return f"{self.field}"

    def _validate_field(self) -> None:
        set_ships = set(self.field.values())
        quantity = len(set_ships)
        if quantity != 10:
            print(f"There must be 10 ships, but are {quantity}")
            return
        ships_by_type = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship in set_ships:
            length = len(ship.decks)
            if length in ships_by_type.keys():
                ships_by_type[length] += 1
        for number_of_decks in ships_by_type:
            if number_of_decks + ships_by_type[number_of_decks] != 5:
                print(f"There must be {5 - number_of_decks} ships, "
                      f"with {number_of_decks} decks")
                return
        for ship in set_ships:
            row_start, column_start = ship.decks[0].row, ship.decks[0].column
            row_end, column_end = ship.decks[-1].row, ship.decks[-1].column
            for row in range(row_start - 1, row_end + 2):
                for column in range(column_start - 1, column_end + 2):
                    if 0 <= row <= 9 and 0 <= column <= 9:
                        if (row_start <= row <= row_end
                                and column_start <= column <= column_end):
                            continue
                        try:
                            if self.field[(row, column)]:
                                print("The ships are not positioned correctly")
                                return
                        except KeyError:
                            pass

    def create_field(self) -> None:
        for start, end in self.ships:
            ship = Ship(start=start, end=end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(row=location[0], column=location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row=location[0], column=location[1])
                    if deck.is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print("\n")
