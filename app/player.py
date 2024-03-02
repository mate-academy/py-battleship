from app.main import Battleship
import random


class Player:
    def __init__(self, name: str, fleet: list[tuple[tuple, tuple]]) -> None:
        self.name = name
        self.battleship = Battleship(fleet)

    def fire_to_pirate(self) -> None:
        pass


class Pirate(Player):
    def __init__(self, fleet: list[tuple[tuple, tuple]]) -> None:
        super().__init__(self.name, fleet)
        self.battleship = Battleship(fleet)