from app.player import Player


class Game:
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

    @staticmethod
    def print_game_field(field: list[tuple[tuple, tuple]]) -> None:
        game_field = [["\U0001F7E6"] * 10 for _ in range(10)]
        for row, col in field:
            print(row, col)

        # for row in game_field:
        #     print(*row)
        # print("-" * 32)

    def add_manual_ship(self) -> None:
        coordinate_of_ship = []
        available_fleet = {1: 4, 2: 3, 3: 2, 4: 1}
        print("Greate!\n"
              "You must place your ships on a 10x10 field\n"
              "The first coordinate of each cell is the number of the row.\n"
              "The second is the number of the column.\n"
              "The upper-left corner has coordinates `(0, 0)`.\n"
              "The lower-right has coordinates `(9, 9)`.\n"
              "\033[1mYou must enter coordinates in the format: "
              "0.0-0.0\033[0m\n")
        start_coordinate = tuple
        end_coordinate = tuple
        coordinate = input().split("-")
        ship = tuple(tuple(map(int, point.split(".")))
                     for point in coordinate)
        count_deck = abs(
            (ship[1][0] - ship[0][0]) - (ship[1][1] - ship[0][1])) + 1
        print(count_deck)
        #TODO: need add validate, finished write def for add ship

    def add_auto_ship(self) -> None:
        pass

    @staticmethod
    def exit() -> None:
        print("-" * 65)
        print("\033[1;31mGoodbye!\033[0m")

    def add_ships(self) -> None:
        fleet = []
        print("\033[1mNow you need to prepare for battle!\033[0m")
        print("You need to place your fleet.")
        print("You can place each ship independently or they can choose their "
              "own place.")
        how_add_ships = ""
        while True:
            how_add_ships = input("How do you want to do it? (M / A) ").lower()
            if how_add_ships == "m":
                print("-" * 65)
                self.add_manual_ship()
                break
            elif how_add_ships == "a":
                print("-" * 65)
                self.add_auto_ship()
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
                how_add_ships = input(
                    "Give your order ").lower()

    @staticmethod
    def greate_player(name: str, fleet: list[tuple[tuple, tuple]]) -> None:
        Player(name, fleet)


game = Game()

game.add_ships()
