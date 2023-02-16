from pprint import pprint

from app.carbon import Carbon
from app.cell import Cell
from app.corpse import Corpse
from app.deck import Deck
from app.ship import Ship


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships_sides = ships
        self.ocean = [[Cell((x, y)) for y in range(10)] for x in range(10)]
        self.field = self._set_ship_coordinates()
        self._validate_field()

    def _set_ship_coordinates(self) -> dict:
        ships = (Ship(ship[0], ship[1]) for ship in self.ships_sides)
        ship_coordinates = {}
        for ship in ships:
            for cord in ship.decks_cord:
                self.ocean[cord[0]][cord[1]] = Deck(cord)
                ship_coordinates[cord] = ship
        return ship_coordinates

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
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
        self._check_the_amount()
        self._check_the_location()

    def _check_the_location(self) -> None:
        for cord_x, cord_y in self.field:
            neighborhood = self._identify_neighbors(cord_x, cord_y)
            for x_n, y_n in neighborhood:
                if (x_n, y_n) in self.field:
                    if self.field[(x_n, y_n)] != self.field[(cord_x, cord_y)]:
                        raise ValueError("Ships can not touch each other")

    @staticmethod
    def _identify_neighbors(
            cord_x: int,
            cord_y: int
    ) -> list[tuple[int, int], tuple[int, int]]:
        return list(
            cord
            for cord in (
                (cord_y - 1, cord_x + 1),
                (cord_x, cord_y + 1),
                (cord_x + 1, cord_y + 1),
                (cord_x - 1, cord_y),
                (cord_x + 1, cord_y),
                (cord_x - 1, cord_y - 1),
                (cord_x, cord_y - 1),
                (cord_x - 1, cord_y + 1),
            )
            if -1 < cord[0] < 10 and -1 < cord[1] < 10
        )

    def _check_the_amount(self) -> None:
        expected = {"4deck": 1, "3deck": 2, "2deck": 3, "1deck": 4}
        available = {"4deck": 0, "3deck": 0, "2deck": 0, "1deck": 0}
        proposed_navy = set(self.field.values())
        for ship in proposed_navy:
            if len(ship.decks_cord) == 4:
                available["4deck"] += 1
            if len(ship.decks_cord) == 3:
                available["3deck"] += 1
            if len(ship.decks_cord) == 2:
                available["2deck"] += 1
            if len(ship.decks_cord) == 1:
                available["1deck"] += 1
        if expected != available or len(proposed_navy) != 10:
            raise ValueError(f"The navy must contain such 10 ships:{expected}")

    def print_field(self) -> None:
        pprint(self.ocean)
