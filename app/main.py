from app.battleship import Battleship


battle_ship = Battleship(
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

print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)
