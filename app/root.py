from app.game import Game
from app.player import Player
from app.player import Pirate
from app.exceptions import ShotInSamePlaceException

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")

    game.print_description_fleet(captain_name)

    player_1 = Player(captain_name, game.add_ships())
    game.clear_fleet()

    pirate = Pirate(game.add_auto_ship())
    game.clear_fleet()

    print()
    while True:
        fire = input("Enter coordinates for the shot (format: 0.0): ")
        try:
            fire_tuple = tuple(int(i) for i in fire.split("."))
            try:
                player_1.fire_to_enemy(fire_tuple, pirate)
            except ShotInSamePlaceException:
                print("\033[1;31mYou've already shot at this place.\033[0m")
        except ValueError:
            print("-" * 65)
            print("\033[1;31mInvalid coordinate format!\033[0m\n"
                  "You must enter coordinates in the format: "
                  "\033[1m0.0\033[0m")
            print("-" * 65)
        print(all(ship.is_drowned for ship in list(pirate.battleship.field.values())))
