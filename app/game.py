import random
from itertools import chain

from app.exceptions import ShipPlacementExeption
from app.exceptions import TotalShipsInFleet


class Game:
    def __init__(self) -> None:
        self.coordinate_of_ship = {1: [], 2: [], 3: [], 4: []}

    @staticmethod
    def print_introduce() -> None:
        name_of_game = "Sea Battle: Pirate Battles"
        print(f"\033[1m{name_of_game.center(65)}\033[0m\n"
              f"{"-" * 65}")
        print("Welcome to the world of adventure and naval battles!\n"
              "You find yourself in the waters of the Caribbean Sea,\n"
              "where thrilling encounters with ruthless pirates await you.\n"
              "Your ship is ready to set sail, and your task is to become an\n"
              "unbeatable captain, defeat enemies, and conquer glory on the\n"
              "seven seas. Beware of enemy ships, use strategy and tactics\n"
              "to emerge victorious in this epic struggle for dominance\n"
              "in the waters of the Caribbean Sea.\n"
              "Get ready for exciting adventures in "
              "\033[1m'Sea Battle: Pirate Battles'\033[0m!")
        print("-" * 65)

    @staticmethod
    def print_description_fleet(captain_name: str) -> None:
        print("-" * 65)
        print(f"Greetings Admiral {captain_name}!")
        print("At your disposal you have:")
        print(" 4 'Sloop' (single-deck ships) - \u26F5")
        print(" 3 'Frigate' (double-deck ships) - \u26F5\u26F5")
        print(" 2 'Linear Corvette' (three-deck ships) - \u26F5\u26F5\u26F5")
        print(" 1 'Armored Galleon' (four-deck ship) "
              "- \u26F5\u26F5\u26F5\u26F5")
        print("-" * 65)

    def _validate_field(self, ship: tuple, count_deck: int,
                        fleet: list[tuple]) -> None:
        if len(self.coordinate_of_ship) == 10:
            raise TotalShipsInFleet("The total number "
                                    "of the ships should be 10")
        if count_deck > 4 or count_deck < 1:
            raise ShipPlacementExeption("The number of decks can "
                                        "be from 1 to 4")
        if count_deck == 1 and len(self.coordinate_of_ship[count_deck]) == 4:
            raise ShipPlacementExeption("There should be 4 single-deck ships")
        if count_deck == 2 and len(self.coordinate_of_ship[count_deck]) == 3:
            raise ShipPlacementExeption("There should be 3 double-deck ships")
        if count_deck == 3 and len(self.coordinate_of_ship[count_deck]) == 2:
            raise ShipPlacementExeption("There should be 2 three-deck ships")
        if count_deck == 4 and len(self.coordinate_of_ship[count_deck]) == 1:
            raise ShipPlacementExeption("There should be 1 four-deck ship")

        fleet_coordinates = set()
        for ship_coords in fleet:
            for row in range(ship_coords[0][0], ship_coords[1][0] + 1):
                for column in range(ship_coords[0][1], ship_coords[1][1] + 1):
                    fleet_coordinates.add((row, column))
        for row in range(ship[0][0] - 1, ship[1][0] + 2):
            for column in range(ship[0][1] - 1, ship[1][1] + 2):
                if (row, column) in fleet_coordinates:
                    raise ShipPlacementExeption("Ships should not be located "
                                                "in neighboring cells")

    @staticmethod
    def print_game_field(field: list[tuple]) -> None:
        game_field = [["\U0001F7E6"] * 10 for _ in range(10)]
        for ship in field:
            start, end = ship
            if start == end:
                game_field[start[0]][start[1]] = "\u26F5"
            if start[0] == end[0]:
                for i in range(abs(start[1] - end[1]) + 1):
                    game_field[start[0]][start[1] + i] = "\u26F5"
            if start[1] == end[1]:
                for i in range(abs(start[0] - end[0]) + 1):
                    game_field[start[0] + i][end[1]] = "\u26F5"
        for row in game_field:
            print(*row)
        print("-" * 32)

    def add_manual_ship(self) -> list:
        fleet = []
        print("Greate!\n"
              "You must place your ships on a 10x10 field\n"
              "The first coordinate of each cell is the number of the row.\n"
              "The second is the number of the column.\n"
              "The upper-left corner has coordinates `(0, 0)`.\n"
              "The lower-right has coordinates `(9, 9)`.\n"
              "\033[1mYou must enter coordinates in the format: "
              "0.0-0.0\033[0m\n")
        while True:
            try:
                coordinate = input("Enter ship coordinates: ").split("-")
                ship = tuple(tuple(map(int, point.split(".")))
                             for point in coordinate)
                try:
                    count_deck = abs((ship[1][0] - ship[0][0])
                                     - (ship[1][1] - ship[0][1])) + 1
                    try:
                        self._validate_field(ship, count_deck, fleet)
                        self.coordinate_of_ship[count_deck].append(ship)
                        fleet = list(chain(*self.coordinate_of_ship.values()))
                        self.print_game_field(fleet)
                        if len(fleet) == 10:
                            print("You have placed all your ships.\n"
                                  "It's time to start the battle!")
                            break
                    except ShipPlacementExeption as e:
                        print(f"{"-" * 65}\n"
                              f"{e}\n"
                              f"{"-" * 65}")
                except IndexError:
                    print("-" * 65)
                    print("\033[1;31mInvalid coordinate format!\033[0m\n"
                          "You must enter coordinates in the format: "
                          "\033[1m0.0-0.0\033[0m")
                    print("-" * 65)
            except ValueError:
                print("-" * 65)
                print("\033[1;31mInvalid coordinate format!\033[0m\n"
                      "You must enter coordinates in the format: "
                      "\033[1m0.0-0.0\033[0m")
                print("-" * 65)
        return fleet

    def _add_ship_direction(
            self,
            all_cells: list[tuple],
            direction: str,
            start_cell: tuple,
            count_deck: int,
            fleet: list[tuple]
    ) -> bool:
        if direction == "row":
            end_cell = (start_cell[0] + (count_deck - 1), start_cell[1])
        elif direction == "column":
            end_cell = (start_cell[0], start_cell[1] + (count_deck - 1))

        if end_cell not in all_cells:
            return False
        ship = (start_cell, end_cell)
        try:
            self._validate_field(ship, count_deck, fleet)
            self.coordinate_of_ship[count_deck].append(ship)
            return True
        except ShipPlacementExeption:
            return False

    def add_auto_ship(self) -> list:
        fleet = []
        all_cells = [(row, column) for row in range(10)
                     for column in range(10)]
        available_decks = [1, 2, 3, 4]

        while True:
            row_or_column = ["row", "column"]

            start_cell = random.choice(all_cells)
            count_deck = random.choice(available_decks)

            move_from_row_or_column = random.choice(row_or_column)

            self._add_ship_direction(all_cells, move_from_row_or_column,
                                     start_cell, count_deck, fleet)
            fleet = list(chain(*self.coordinate_of_ship.values()))
            if len(fleet) == 10:
                return fleet

    @staticmethod
    def exit() -> None:
        print("-" * 65)
        print("\033[1;31mGoodbye!\033[0m")

    def add_ships(self) -> list:
        fleet = []
        print("\033[1mNow you need to prepare for battle!\033[0m")
        print("You need to place your fleet.")
        print("You can place each ship independently or they can choose their "
              "own place.")
        while True:
            how_add_ships = input("How do you want to do it? (M / A) ").lower()
            if how_add_ships == "m":
                print("-" * 65)
                fleet = self.add_manual_ship()
                break
            elif how_add_ships == "a":
                print("-" * 65)
                fleet = self.add_auto_ship()
                self.print_game_field(fleet)
                print("-" * 65)
                break
            elif how_add_ships == "e":
                self.exit()
                break
            else:
                print("-" * 65)
                print("\033[1;31mYou can use only two commands 'M' (manual) "
                      "or 'A' (auto)\033[0m")
                print("Or 'E' for exit from game")
                print("-" * 65)
        return fleet

    def clear_fleet(self) -> None:
        self.coordinate_of_ship = {1: [], 2: [], 3: [], 4: []}
