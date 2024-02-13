from typing import List
from app.ship import Ship


def build_battleships(coordinates: List[tuple]) -> list:
    fleet = []
    for coordinate in coordinates:
        built_ship = Ship(coordinate[0], coordinate[1])
        fleet.append(built_ship)
    return fleet
