from app.main import Battleship


def test_battleship():
    battle_ship = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )
    assert battle_ship.fire((0, 4)) == "Miss!"
    assert battle_ship.fire((1, 7)) == "Miss!"
    assert battle_ship.fire((2, 0)) == "Hit!"
    assert battle_ship.fire((2, 1)) == "Hit!"
    assert battle_ship.fire((2, 2)) == "Hit!"
    assert battle_ship.fire((2, 3)) == "Sunk!"
    assert battle_ship.fire((4, 3)) == "Miss!"
    assert battle_ship.fire((4, 5)) == "Hit!"
    assert battle_ship.fire((5, 5)) == "Miss!"
    assert battle_ship.fire((4, 6)) == "Sunk!"
    assert battle_ship.fire((9, 5)) == "Sunk!"
    assert battle_ship.fire((9, 6)) == "Miss!"
    assert battle_ship.fire((9, 5)) == "Sunk!"
