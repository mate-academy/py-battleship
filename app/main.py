from app.battleship import Battleship
from app.constants import SYMBOL_LEGEND_LINES
from app.game_loop import play_game
from app.ship_generator import generate_random_ship_placements


def print_symbol_legend() -> None:
    print("\nSYMBOL LEGEND:")
    print("\n".join(SYMBOL_LEGEND_LINES))


def main() -> None:
    ship_placements = generate_random_ship_placements()
    game = Battleship(ship_placements)

    print("\nWelcome to Battleship!")
    print_symbol_legend()
    print(f"\n{game}")

    play_game(game)


if __name__ == "__main__":
    main()
