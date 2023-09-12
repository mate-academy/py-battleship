from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.ship_deck = self.init_ship_decks()

    def init_ship_decks(self) -> List[Deck]:
        list_decks = []

        if self.start[0] == self.start[1] and self.end[0] == self.end[1]:
            list_decks.append(Deck(self.start[0], self.start[1]))
        else:
            if self.start[0] == self.end[0]:
                # for x
                for work_y in range(self.start[1], self.end[1] + 1):
                    list_decks.append(Deck(self.start[0], work_y))
            if self.start[1] == self.end[1]:
                # for y
                for work_x in range(self.start[0], self.end[0] + 1):
                    list_decks.append(Deck(work_x, self.start[1]))

        return list_decks

    def get_deck(self, row: int, column: int) -> bool:
        # Find the corresponding deck in the list
        for target_deck in self.ship_deck:
            if (row, column) == (target_deck.row, target_deck.column):
                return target_deck.is_alive

    def alive_or_dead_ship(self) -> bool:
        ship_info_res = []
        for ship_info in self.ship_deck:
            ship_info_res.append(ship_info.is_alive)
        alive_or_dead = any(ship_info_res)
        return alive_or_dead

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for target_deck in self.ship_deck:
            if (row, column) == (target_deck.row, target_deck.column):
                if target_deck.is_alive:
                    target_deck.is_alive = False


class Battleship:

    Ships_in_battle = []
    ship_all_place = []

    def __init__(self, ships: List[Tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = ships
        self.init_ships_in_battle()
        self.init_all_place_ship()

    def init_ships_in_battle(self) -> None:
        for work_ship in self.ships:
            self.Ships_in_battle.append(Ship(work_ship[0], work_ship[1]))

    def init_all_place_ship(self) -> None:
        for data_ship in self.ships:
            if (
                    data_ship[0][0] == data_ship[1][0]
                    and data_ship[0][1] == data_ship[1][1]
            ):
                self.ship_all_place.append((data_ship[0][0], data_ship[0][1]))
            else:
                if data_ship[0][0] == data_ship[1][0]:
                    # for x
                    for work_y in range(data_ship[0][1], data_ship[1][1] + 1):
                        self.ship_all_place.append((data_ship[0][0], work_y))
                if data_ship[0][1] == data_ship[1][1]:
                    # for y
                    for work_x in range(data_ship[0][0], data_ship[1][0] + 1):
                        self.ship_all_place.append((work_x, data_ship[0][1]))

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        if location not in self.ship_all_place:
            return "Miss!"
        for target_ship in self.Ships_in_battle:
            if target_ship.get_deck(location[0], location[1]):
                target_ship.fire(location[0], location[1])
                if target_ship.alive_or_dead_ship():
                    return "Hit!"
                else:
                    return "Sunk!"
