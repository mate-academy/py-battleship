import pytest
from pytest import CaptureFixture

from app.main import Battleship, Ship


@pytest.fixture
def fleet() -> list:
    return [
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


def test_reversed_endpoints_and_complete_fleet(fleet: list) -> None:
    battle = Battleship([(end, start) for start, end in fleet])
    assert len(battle.field) == 20
    for ship in battle.ships:
        for index, deck in enumerate(ship.decks):
            expected = "Sunk!" if index == len(ship.decks) - 1 else "Hit!"
            assert battle.fire((deck.row, deck.column)) == expected
        assert ship.is_drowned
    assert all(not deck.is_alive
               for ship in battle.ships for deck in ship.decks)


def test_repeated_shot_cannot_sink_another_deck(fleet: list) -> None:
    battle = Battleship(fleet)
    assert battle.fire((0, 0)) == "Hit!"
    assert battle.fire((0, 0)) == "Miss!"
    assert not battle.field[(0, 0)].is_drowned


@pytest.mark.parametrize("invalid_index", [0, 7, 9])
def test_wrong_fleet_size_is_rejected(
    fleet: list, invalid_index: int
) -> None:
    fleet.pop(invalid_index)
    with pytest.raises(ValueError):
        Battleship(fleet)


def test_diagonal_neighbors_are_rejected(fleet: list) -> None:
    fleet[7] = ((8, 8), (8, 8))
    with pytest.raises(ValueError):
        Battleship(fleet)


def test_outside_board_is_rejected(fleet: list) -> None:
    fleet[7] = ((10, 7), (10, 7))
    with pytest.raises(ValueError):
        Battleship(fleet)


def test_overlap_is_rejected(fleet: list) -> None:
    fleet[7] = ((9, 9), (9, 9))
    with pytest.raises(ValueError):
        Battleship(fleet)


def test_diagonal_ship_is_rejected() -> None:
    with pytest.raises(ValueError):
        Ship((0, 0), (1, 1))


def test_field_display(fleet: list, capsys: CaptureFixture[str]) -> None:
    battle = Battleship(fleet)
    battle.fire((0, 0))
    battle.fire((9, 9))
    battle.print_field()
    rows = [line.split("\t") for line in capsys.readouterr().out.splitlines()]
    assert len(rows) == 10
    assert all(len(row) == 10 for row in rows)
    assert rows[0][:5] == ["*", "□", "□", "□", "~"]
    assert rows[9][9] == "x"
