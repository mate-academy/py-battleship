from app.game import Game
from app.player import Pirate
from app.player import Player

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")

    game.print_description_fleet(captain_name)

    player_1 = Player(captain_name, game.add_ships())
    game.clear_fleet()

    pirate = Pirate(game.choose_pirate_name(), game.add_auto_ship())
    game.clear_fleet()

    print(f"{"-" * 65}\n"
          f"Your enemy is \U0001F3F4{pirate.name}\U0001F3F4\n"
          f"{"-" * 65}")

    game.play_game(player_1, pirate)
