from typing import List

from app.history_shoots import history_shoots
from app.ship import Ship


class Battleship:
    def __init__(self, ships: List[tuple]):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.fleet = self._create_fleet()

    def _create_fleet(self):
        return {
            cord: Ship(
                start=cord[0],
                end=cord[1]
            )
            for cord in self.ships
        }

    @history_shoots
    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.fleet.values():
            deck = ship.get_deck(location[0], location[1])

            if deck and not ship.chech_sunk():
                return ship.hit_in_deck(deck)
            elif deck and ship.chech_sunk():
                return ship.sunk_ship(deck)

        return ship.miss_in_ship()
