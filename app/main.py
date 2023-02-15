from pprint import pprint
from typing import Tuple, List

from app.carbon import Carbon
from app.cell import Cell
from app.corpse import Corpse
from app.deck import Deck
from app.ship import Ship


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ocean = [[Cell((x, y)) for y in range(10)] for x in range(10)]
        self.field = self.set_ship_coordinates(ships)
        self._validate_field()

    def set_ship_coordinates(self, ships: Tuple[tuple]) -> dict:
        ships = (Ship(ship[0], ship[1]) for ship in ships)
        ship_coordinates = {}
        for ship in ships:
            for cord in ship.decks_cord:
                self.ocean[cord[0]][cord[1]] = Deck(cord)
                ship_coordinates[cord] = ship
        return ship_coordinates

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            ship.kicks.add(location)
            self.ocean[location[0]][location[1]] = Carbon(location)
            if set(ship.decks_cord) == ship.kicks:
                for cord in ship.decks_cord:
                    self.ocean[cord[0]][cord[1]] = Corpse(cord)
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        count4 = 0
        count3 = 0
        count2 = 0
        count1 = 0
        expected = {"4-decks": 1, "3-decks": 2, "2-decks": 3, "1-decks": 4}

        for ship in set(self.field.values()):
            if len(ship.decks_cord) == 4:
                count4 += 1
            if len(ship.decks_cord) == 3:
                count3 += 1
            if len(ship.decks_cord) == 2:
                count2 += 1
            if len(ship.decks_cord) == 1:
                count1 += 1
        available = {
            "4-decks": count4,
            "3-decks": count3,
            "2-decks": count2,
            "1-decks": count1,
        }
        if expected != available:
            raise ValueError(f"Must be {expected}")
        for cord_x, cord_y in self.field:
            neighborhood = (
                (cord_y - 1, cord_x + 1),
                (cord_x, cord_y + 1),
                (cord_x + 1, cord_y + 1),
                (cord_x - 1, cord_y),
                (cord_x + 1, cord_y),
                (cord_x - 1, cord_y - 1),
                (cord_x, cord_y - 1),
                (cord_x - 1, cord_y + 1),
            )
            neighborhood = (
                cord for cord in neighborhood
                if 0 <= cord[0] <= 9 and 0 <= cord[1] <= 9
            )
            for x_n, y_n in neighborhood:
                if (x_n, y_n) in self.field:
                    if self.field[(x_n, y_n)] != self.field[(cord_x, cord_y)]:
                        raise ValueError(
                            "Ships are not allowed to touch each other"
                        )


ships = [
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

battle_ship = Battleship(ships)
battle_ship.fire((2, 0))
battle_ship.fire((9, 9))
pprint(battle_ship.ocean)
