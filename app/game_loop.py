from app.battleship import Battleship
from app.input_utils import get_coordinate


def play_game(game: Battleship) -> None:
    while not game.is_game_over:
        try:
            coordinate = get_coordinate()

            if coordinate is None:
                print("\nGame aborted.")
                return

            row, col = coordinate

            result = game.fire((row, col))
            print(result)
            print(f"\n{game}")

        except ValueError as error:
            print(error)
        except KeyboardInterrupt:
            print("\nGame aborted.")
            return

    print("\n🔥 All ships are sunk! Game over!")
