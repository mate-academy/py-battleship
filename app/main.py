from typing import List, Tuple


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    def __init__(self, start: tuple, end: tuple, is_drowned=False):
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

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:

    Ships_in_battle = []
    ship_all_place = []

    def __init__(self, ships: List[Tuple]):
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
            if data_ship[0][0] == data_ship[1][0] and data_ship[0][1] == data_ship[1][1]:
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
        ooo = 0

        if location not in self.ship_all_place:
            return "Miss!"
        for target_ship in self.Ships_in_battle:
            # тут обработать палубы при помощи функции get_deck которая вернет статус палуб и статус самого корабля
            for target_deck in target_ship.ship_deck:
                yyyy = (target_deck.row, target_deck.column)
                if location == (target_deck.row, target_deck.column):
                    if target_deck.is_alive:
                        # тут обработку подбитой палубы
                        return "Hit!"
                    else:
                        return "Miss!"





battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
    # [((2, 8), (2, 9)), ((2, 0), (4, 0))]
)

print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)

ttt = 0
