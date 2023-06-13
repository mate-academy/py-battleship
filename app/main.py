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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

    @staticmethod
    def __create_decks(start: tuple, end: tuple) -> list[Deck]:
        head, tail, deck_coordinates = start, end, []
        common_coordinate = "row" if head[0] in tail else "column"
        while head != tail:
            deck_coordinates.append((head[0], head[1]))
            if common_coordinate == "row":
                head = (head[0], head[1] + 1)
            else:
                head = (head[0] + 1, head[1])
        deck_coordinates.append((head[0], head[1]))
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
        all_ships_with_coordinates = {}
        ships = [Ship(start, end) for start, end in self.ships]
        for ship in ships:
            for deck in ship.decks:
                all_ships_with_coordinates[deck.coordinates] = ship
        return all_ships_with_coordinates

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

    def print_field(self) -> None:
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
        for row in field:
            for column in row:
                print(column, end=" ")
            print()

    def __validate_field(self) -> None:
        data = set(self.__create_ships().values())
        if len(self.ships) != 10:
            raise Exception("The number of ships should be equal to 10")
        self.__is_another_ship_in_neighbor_cell(data)
        self.__correct_num_of_ships_with_definite_decks_num(data)

    @staticmethod
    def __correct_num_of_ships_with_definite_decks_num(
            data: set[Ship]
    ) -> None:
        num_of_decs_and_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in data:
            num_of_decks = len(ship.decks)
            if num_of_decks in num_of_decs_and_ships:
                num_of_decs_and_ships[num_of_decks] += 1
                continue
            raise Exception(
                f"ship can't has {num_of_decks} decks,"
                f" the value must be in range 1...4"
            )
        assert num_of_decs_and_ships == {1: 4, 2: 3, 3: 2, 4: 1}, (
            "should be 4 single-deck ships; 3 double-deck ships;"
            " 2 three-deck ships; 1 four-deck ship;"
        )

    def __is_another_ship_in_neighbor_cell(self, data: set[Ship]) -> None:
        for ship in data:
            for deck in ship.decks:
                for row in range(-1, 2):
                    for column in range(-1, 2):
                        if row == 0 and column == 0:
                            continue
                        neighbor_row = deck.coordinates[0] + row
                        neighbor_column = deck.coordinates[1] + column
                        if neighbor_row > 9 or neighbor_column > 9:
                            continue
                        if (neighbor_row, neighbor_column) in self.field:
                            current_ship = self.field.get(
                                (neighbor_row, neighbor_column)
                            )
                            all_decks_of_current_ship = [
                                deck.coordinates for deck in current_ship.decks
                            ]
                            all_decks_of_ship = [
                                deck.coordinates for deck in ship.decks
                            ]
                            if all_decks_of_current_ship != all_decks_of_ship:
                                raise Exception(
                                    "ships shouldn't be located"
                                    " in the neighboring cells"
                                )


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
print(battle_ship.print_field())
