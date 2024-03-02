from app.game import Game
from app.player import Player
import random

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")

    game.print_description_fleet(captain_name)

    player_1 = Player(captain_name, game.add_ships())

    pirate_names = [
        "Captain Jack Sparrow", "Captain Hector Barbossa",
        "Davy Jones", "Captain Edward Teague"
    ]
    pirate_name = random.choice(pirate_names)
    pirate = Player(pirate_name, game.add_auto_ship())

    print(player_1.name)
    print("-"*30)
    print(pirate.name)
