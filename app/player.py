from app.main import Battleship


class Player:
    def __init__(self, name: str, fleet: list[tuple[tuple, tuple]]) -> None:
        self.name = name
        self.battleship = Battleship(fleet)

    def my_fleet(self) -> None:
        self.fleet = {
            "single_deck": 0, "double_deck": 0, "three_deck": 0,
            "four_deck": 0
        }

    def add_ship(self, ship_coordinates: tuple[tuple, tuple]) -> None:
        pass
