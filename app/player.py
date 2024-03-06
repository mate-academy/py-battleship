from __future__ import annotations

import random

from app.main import Battleship
from app.exceptions import ShotInSamePlaceException


class Player:
    def __init__(self, name: str, fleet: list[tuple[tuple, tuple]]) -> None:
        self.name = name
        self.battleship = Battleship(fleet)
        self.list_of_fire = {"miss": [], "hit": []}

    def fire_to_enemy(
            self,
            location: tuple[int, int],
            enemy: Player
    ) -> None:
        if (location in self.list_of_fire["miss"]
                or location in self.list_of_fire["hit"]):
            raise ShotInSamePlaceException
        fire = enemy.battleship.fire(location)
        if fire == "Miss!":
            self.list_of_fire["miss"].append(location)
        else:
            print(f"{"-" * 32}\n{fire}")
            self.list_of_fire["hit"].append(location)

    def print_field_fires(self) -> None:
        game_field = [["\U0001F7E6"] * 10 for _ in range(10)]
        for row, col in self.list_of_fire["miss"]:
            game_field[row][col] = "\u274C"
        for row, col in self.list_of_fire["hit"]:
            game_field[row][col] = "\U0001F4A5"
        for row in game_field:
            print(*row)


class Pirate(Player):
    def __init__(self, name: str, fleet: list[tuple[tuple, tuple]]) -> None:
        super().__init__(name, fleet)
        self.battleship = Battleship(fleet)
        self.list_of_fire = {"miss": [], "hit": []}

    @staticmethod
    def choose_cell_for_shoot() -> tuple[int, int]:
        all_cells = [(row, column) for row in range(10)
                     for column in range(10)]
        return random.choice(all_cells)
