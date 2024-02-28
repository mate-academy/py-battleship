from app.game import Game

if __name__ == "__main__":
    game = Game()
    game.print_introduce()

    captain_name = input("\033[1mWhat is your name, Admiral?\033[0m ")
    game.print_description_fleet(captain_name)

    game.add_ships()

