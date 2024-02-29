from app.game import Game
from app.player import Player

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")
    game.print_description_fleet(captain_name)

    plaeyer_1 = Player(captain_name, game.add_ships())

    print(plaeyer_1.battleship)
