from typing import Union, Tuple

from tabulate import tabulate


class Deck:
    def __init__(
            self, row: int, column: int, is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (
            f"ID: {id(self)}\n"
            f"Coordinates: ({self.row},{self.column})\n"
            f"is_alive: {self.is_alive}"
        )


class Ship:
    def __init__(
            self, start: Tuple[int, int], end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.direction = None
        self.get_axis()
        self.fill_decks()

    def fill_decks(self) -> None:
        if self.start == self.end:
            self.decks.append(Deck(row=self.start[0], column=self.start[1]))
        if self.start[0] == self.end[0]:
            self.decks = [
                Deck(row=self.start[0], column=coord)
                for coord in range(self.start[1], self.end[1] + 1)
            ]
            return

        self.decks = [Deck(row=coord, column=self.start[1]) for coord
                      in range(self.start[0], self.end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            damaged_decks = 0
            deck.is_alive = False
            for deck in self.decks:
                if not deck.is_alive:
                    damaged_decks += 1
            if damaged_decks == len(self.decks):
                self.is_drowned = True

    def get_axis(self) -> None:
        if self.start == self.end:
            self.direction = "single_point"
            return
        if self.start[0] == self.end[0]:
            self.direction = "x"
            return
        self.direction = "y"

    def get_neighbors(self, neighboring_cells):
        counter = len(self.decks)
        ship_neighbors = []
        for deck in self.decks:
            if (deck.row, deck.column) in neighboring_cells:
                return []
            counter -= 1

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
                if counter != 0:
                    deck_neighbors[5] = None
                ship_neighbors.extend(deck_neighbors)

            if self.direction == "y":
                if counter != 0:
                    deck_neighbors[7] = None
                ship_neighbors.extend(deck_neighbors)

        return ship_neighbors

    def __repr__(self) -> str:
        return (
            f"ID: {id(self)}\n"
            f"Direction: {self.direction}\n"
            f"Len: {len(self.decks)}\n"
        )


class Battleship:
    def __init__(self, ships: list[tuple]):
        self.field = {}
        for coord in ships:  # debug
            ship = Ship(start=coord[0], end=coord[1])

            for deck in ship.decks:
                self.field[deck] = ship

        if self._validate_input():
            self.print_field()

    def fire(self, location: tuple):  # Loop is not needed. Just check:
        print(f"\n\n\nFIRE TO {location} location!")

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

            placement_check = unique_ship.get_neighbors(neighboring_cells)
            if not placement_check:
                current_session["placement_error"] = True

            neighboring_cells.extend(placement_check)

            for deck in unique_ship.decks:
                coordinates = (deck.row, deck.column)
                neighboring_cells.append(coordinates)

            if len(unique_ship.decks) == 4:
                current_session["four_deck_ships"] += 1
            if len(unique_ship.decks) == 3:
                current_session["three_deck_ships"] += 1
            if len(unique_ship.decks) == 2:
                current_session["double_deck_counter"] += 1
            if len(unique_ship.decks) == 1:
                current_session["single_deck_counter"] += 1

        if current_session == requirements:
            print(f"{'*' * 14} FIELD VALID {'*' * 14}")
            return True

        for requirements, result in current_session.items():
            print(f"{' '.join(str(requirements).split(sep='_')).capitalize()}"
                  f" : {result}")


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

    while True:
        user_input = input("\nCoordinates to hit:   ")
        if "exit" in user_input.lower():
            break
        coordinates = []
        for num in user_input:
            if num.isnumeric():
                coordinates.append(int(num))

        battle_ship.fire(tuple(coordinates))
