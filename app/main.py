from __future__ import annotations
from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.coordinates = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = self.__create_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def __create_decks(start: tuple, end: tuple) -> list[Deck]:
        deck_coordinates = []
        common_coordinate = "row" if start[0] in end else "column"
        while start != end:
            deck_coordinates.append((start[0], start[1]))
            if common_coordinate == "row":
                start = (start[0], start[1] + 1)
            else:
                start = (start[0] + 1, start[1])
        deck_coordinates.append((start[0], start[1]))
        deck_instances = [
            Deck(row, column) for row, column in deck_coordinates
        ]
        return deck_instances

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.coordinates == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.field = self.__create_ships()
        self.__validate_field()

    def __create_ships(self) -> dict:
        deck_and_its_ship = {}
        ships = [Ship(start, end) for start, end in self.ships]
        for ship in ships:
            for deck in ship.decks:
                deck_and_its_ship[deck.coordinates] = ship
        return deck_and_its_ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(location[0], location[1])
            if any(deck.is_alive for deck in ship.decks):
                return "Hit!"
            return "Sunk!"
        return "Miss!"

    def __create_field(self) -> list[list[str]]:
        field = [["~" for i in range(10)] for j in range(10)]
        for ship in self.field.values():
            for deck in ship.decks:
                if not ship.is_drowned:
                    if deck.is_alive:
                        field[deck.coordinates[0]][
                            deck.coordinates[1]] = "\u25A1"
                    else:
                        field[deck.coordinates[0]][deck.coordinates[1]] = "*"
                    continue
                field[deck.coordinates[0]][deck.coordinates[1]] = "x"
        return field

    def print_field(self) -> None:
        field = self.__create_field()
        for row in field:
            for column in row:
                print(column, end=" ")
            print()

    def __validate_field(self) -> None:
        if len(self.ships) != 10:
            raise Exception("The number of ships should be equal to 10")
        self.__is_another_ship_in_neighbor_cell()
        self.__correct_num_of_ships_with_definite_decks_num()

    def __correct_num_of_ships_with_definite_decks_num(self) -> None:
        data = set(self.__create_ships().values())
        num_of_ships_and_num_of_deck = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in data:
            num_of_decks = len(ship.decks)
            if num_of_decks in num_of_ships_and_num_of_deck:
                num_of_ships_and_num_of_deck[num_of_decks] += 1
                continue
            raise Exception(
                f"ship can't has {num_of_decks} decks,"
                f" the value must be in range 1...4"
            )
        assert num_of_ships_and_num_of_deck == {1: 4, 2: 3, 3: 2, 4: 1}, (
            "should be 4 single-deck ships; 3 double-deck ships;"
            " 2 three-deck ships; 1 four-deck ship;"
        )

    def __is_another_ship_in_neighbor_cell(self) -> None:
        for deck in self.field:
            for row, col in [
                (-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)
            ]:
                neighbor = (deck[0] + row, deck[1] + col)
                ship_of_neighbor = self.field.get(neighbor)
                ship_of_deck = self.field.get(deck)
                if neighbor in self.field and ship_of_deck != ship_of_neighbor:
                    raise Exception(
                        "ships shouldn't be located in the neighboring cells"
                    )
