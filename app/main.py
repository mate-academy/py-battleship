import numpy as np


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.is_alive = is_alive
        self.row = row
        self.column = column


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = {
                (start[0], index): Deck(start[0], index)
                for index in range(start[1], end[1] + 1)
            }
        if start[1] == end[1]:
            self.decks = {
                (index, start[1]): Deck(index, start[1])
                for index in range(start[0], end[0] + 1)
            }

    def fire(self, location: tuple) -> None:
        self.decks[location].is_alive = False
        deck_status = []

        for deck in self.decks.values():
            deck_status.append(deck.is_alive)

        if not any(deck_status):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship_coords, ship_instance in self.field.items():
            start, end = ship_coords

            if start <= location <= end:
                ship_instance.fire(location)

                if ship_instance.is_drowned:
                    return "Sunk!"
                elif not ship_instance.is_drowned:
                    return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        battle_field = np.full((10, 10), "~")

        for ship in self.field.values():

            for deck_position, deck in ship.decks.items():

                if ship.is_drowned:
                    battle_field[deck_position] = "X"
                elif deck.is_alive and not ship.is_drowned:
                    battle_field[deck_position] = u"\u25A1"
                elif not deck.is_alive and not ship.is_drowned:
                    battle_field[deck_position] = "*"

        print(battle_field)
