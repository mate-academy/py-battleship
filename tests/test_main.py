import pytest
from contextlib import redirect_stdout
from io import StringIO

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


def test_battleship_wrong_ship_shape():
    with pytest.raises(AssertionError) as exc_info:
        Battleship(
            ships=[
                ((2, 0), (3, 3)),
                ((4, 5), (4, 6)),
                ((3, 8), (3, 9)),
                ((6, 4), (6, 4)),
                ((6, 8), (6, 9)),
                ((9, 9), (9, 9)),
                ((9, 3), (9, 3)),
                ((9, 7), (9, 7)),
                ((4, 2), (4, 2)),
                ((1, 6), (1, 6))
            ]
        )

    assert str(exc_info.value) == "wrong shape"


def test_battleship_wrong_number_of_ships():
    with pytest.raises(AssertionError) as exc_info:
        Battleship(
            ships=[
                ((2, 0), (2, 3)),
                ((4, 3), (4, 6)),
                ((3, 8), (3, 9)),
                ((6, 0), (8, 0)),
                ((6, 4), (6, 6)),
                ((6, 8), (6, 9)),
                ((9, 9), (9, 9)),
                ((9, 5), (9, 5)),
            ]
        )

    assert str(exc_info.value) == "must be exactly 10 ships on the field"


def test_battleship_too_long_ship():
    with pytest.raises(AssertionError) as exc_info:
        Battleship(
            ships=[
                ((2, 0), (2, 4)),
                ((4, 5), (4, 6)),
                ((3, 8), (3, 9)),
                ((6, 0), (8, 0)),
                ((6, 5), (6, 6)),
                ((6, 8), (6, 9)),
                ((9, 9), (9, 9)),
                ((9, 5), (9, 5)),
                ((9, 3), (9, 3)),
                ((9, 7), (9, 7)),
            ]
        )

    assert str(exc_info.value) == "ship with 5 decks not allowed"


def test_battleship_ships_are_too_close():
    with pytest.raises(AssertionError) as exc_info:
        Battleship(
            ships=[
                ((2, 0), (2, 3)),
                ((5, 5), (5, 6)),
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

    assert str(exc_info.value) == "ship is too close to another"

def test_battleship_print_field():
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

    sout = StringIO()
    with redirect_stdout(sout):
        battle_ship.print_field()

    assert sout.getvalue() == """~ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ □ □ □ ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ □ □
~ ~ ~ ~ ~ □ □ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ □ □ □ ~ □ □
□ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ □ ~ □ ~ □ ~ □
"""

    assert battle_ship.fire((0, 4)) == "Miss!"
    assert battle_ship.fire((1, 7)) == "Miss!"
    assert battle_ship.fire((2, 0)) == "Hit!"
    assert battle_ship.fire((2, 1)) == "Hit!"
    assert battle_ship.fire((2, 2)) == "Hit!"
    assert battle_ship.fire((2, 3)) == "Sunk!"
    assert battle_ship.fire((4, 3)) == "Miss!"
    assert battle_ship.fire((4, 5)) == "Hit!"

    sout = StringIO()
    with redirect_stdout(sout):
        battle_ship.print_field()

    assert sout.getvalue() == """~ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
x x x x ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ □ □
~ ~ ~ ~ ~ * □ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ □ □ □ ~ □ □
□ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ □ ~ □ ~ □ ~ □
"""

    assert battle_ship.fire((5, 5)) == "Miss!"
    assert battle_ship.fire((4, 6)) == "Sunk!"
    assert battle_ship.fire((9, 5)) == "Sunk!"
    assert battle_ship.fire((9, 6)) == "Miss!"
    assert battle_ship.fire((7, 0)) == "Hit!"
    assert battle_ship.fire((6, 9)) == "Hit!"

    sout = StringIO()
    with redirect_stdout(sout):
        battle_ship.print_field()

    assert sout.getvalue() == """~ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
x x x x ~ ~ ~ ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ □ □
~ ~ ~ ~ ~ x x ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ □ □ □ ~ □ *
* ~ ~ ~ ~ ~ ~ ~ ~ ~
□ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ □ ~ x ~ □ ~ □
"""
