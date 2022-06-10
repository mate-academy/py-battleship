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
        self.field_size = (9, 9)
        self.field = self._create_field()
        self.icon_deck = u"\u25A1"

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
            deck = ship.get_deck(*location)

            if deck and not ship.check_sunk():
                self._to_mark_hit_deck(location)
                return ship.hit_in_deck(deck)
            elif deck and ship.check_sunk():
                self._to_mark_destroy_ship(location)

                return ship.sunk_ship(deck)

        return ship.miss_in_ship()

    def _create_field(self):
        return [
            {
                (hight, width): "~" for width in range(self.field_size[1] + 1)
            }
            for hight in range(self.field_size[0] + 1)
        ]

    def set_ships_on_field(self):
        list_all_decks_cord = [
            (deck.row, deck.column)
            for ship in self.fleet.values()
            for deck in ship.decks
        ]
        for row in self.field:
            for cord in list_all_decks_cord:
                if cord in row:
                    row[cord] = self.icon_deck

    def _to_mark_hit_deck(self, location: tuple):
        for row in self.field:
            if location in row:
                row[location] = "*"

    def _to_mark_destroy_ship(self, location: tuple):
        for row in self.field:
            if location in row:
                row[location] = "X"

    def print_field(self):
        for line in self.field:
            print(*list(line.values()), sep="   ")


if __name__ == '__main__':
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
    battle_ship.print_field()
    battle_ship.set_ships_on_field()
    print("--" * 100)
    battle_ship.print_field()
    print(battle_ship.fire((0, 4)) == "Miss!")
    print(battle_ship.fire((1, 7)) == "Miss!")
    print(battle_ship.fire((2, 0)) == "Hit!")
    print(battle_ship.fire((2, 1)) == "Hit!")
    print(battle_ship.fire((2, 2)) == "Hit!")
    print(battle_ship.fire((2, 3)) == "Sunk!")
    print(battle_ship.fire((4, 3)) == "Miss!")
    print(battle_ship.fire((4, 5)) == "Hit!")
    print(battle_ship.fire((5, 5)) == "Miss!")
    print(battle_ship.fire((4, 6)) == "Sunk!")
    print(battle_ship.fire((9, 5)) == "Sunk!")
    print(battle_ship.fire((9, 6)) == "Miss!")
    print(battle_ship.fire((9, 5)) == "Sunk!")
    print("--" * 100)
    battle_ship.print_field()
