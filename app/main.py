"""The entry point of the application."""
from app.battleship import Battleship, Blueprint


def play(ships: list[Blueprint]) -> None:
    """
    Play the game.

    :param ships: a list of ships to be placed on the field
    """
    try:
        battle_ship = Battleship(ships)
    except ValueError as e:
        print(e)
        return
    battle_ship.print_field()

    while True:
        try:
            row = int(input(
                "Enter row, must be int value smaller "
                + f"than {battle_ship.rows_count}: "
            ).strip())
            column = int(input(
                "Enter column, must be int value smaller "
                + f"than {battle_ship.columns_count}: "
            ).strip())
        except ValueError:
            print("Cannot create point with invalid data!")
            continue

        except KeyboardInterrupt:
            print("\nBye!")
            break
        else:
            try:
                print(battle_ship.fire((row, column)))
            except ValueError as e:
                print(e)
                continue

            battle_ship.print_field()
            if battle_ship.is_fleet_drowned():
                print("Game Over!")
                break


if __name__ == "__main__":
    play(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )
