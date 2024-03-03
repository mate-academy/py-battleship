from app.game import Game
from app.player import Player
from app.player import Pirate

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")

    game.print_description_fleet(captain_name)

    player_1 = Player(captain_name, game.add_ships())
    game.clear_fleet()

    pirate = Pirate(game.add_auto_ship())
    game.clear_fleet()

    print(list(pirate.battleship.field.values()))
    # while True:
    #     fire = input("Enter coordinates for the shot: ")
    #     fire_tuple = tuple(int(i) for i in fire.split("."))
    #     player_1.fire_to_pirate(fire_tuple, pirate)
    #     break
