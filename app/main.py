from __future__ import annotations
from random import randint, choice

RANK = 10
directions = ["s", "e"]
alive_deck = u"\u25A1"


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:

    ships_created = []

    def get_ship(self, two_points: tuple) -> Ship:
        nose, tail = two_points[0], two_points[1]
        for one_ship in Ship.ships_created:
            if one_ship.start == nose and one_ship.end == tail:
                return one_ship

    def change_deck_status(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned:
                 bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        starting_x = start[0]
        starting_y = start[1]
        ending_x = end[0]
        ending_y = end[1]
        self.decks = []
        for i in range(starting_x, ending_x + 1):
            for j_index in range(starting_y, ending_y + 1):
                new_deck = Deck(i, j_index, True)
                self.decks.append(new_deck)

        Ship.ships_created.append(self)

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        pass

    def fire(self, row: int, column: int) -> bool:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        nose, tail = self.start, self.end
        if nose[0] <= row <= tail[0] and nose[1] <= column <= tail[1]:
            self.change_deck_status(row, column)
            self.change_ship_status()
            return True
        return False

    def change_ship_status(self) -> None:
        ship_is_alive = False
        for deck in self.decks:
            ship_is_alive |= deck.is_alive
            if ship_is_alive:
                return
        self.is_drowned = True


class Battleship:

    ships = list[tuple]

    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        for one_ship in self.ships:
            Ship(one_ship[0], one_ship[1], False)

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.ships:
            ship_instance = Ship.get_ship(self, ship)
            if ship_instance.fire(location[0], location[1]):
                if ship_instance.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"  # No hit found


class Seafield():

    sea_cells: dict[tuple]
    ships: list[Ship]

    def one_ship_comes(self, one_ship_list: Ship) -> None:

        first_deck = one_ship_list.decks[0]
        last_deck = one_ship_list.decks[-1]
        nose = tuple([first_deck.row, first_deck.column])
        tail = tuple([last_deck.row, last_deck.column])
        self.allocate_on_seafield(nose, tail)

    def clean(self) -> None:
        self.sea_cells = dict()
        for irow in range(RANK):
            for icol in range(RANK):
                one_cell = tuple([irow, icol])
                self.sea_cells[one_cell] = "~"

    def ships_conversion(self) -> list[tuple]:
        result = []
        for ship in self.ships:
            one_ship_tuple = tuple([ship.start, ship.end])
            result.append(one_ship_tuple)
        return result

    def __init__(self) -> None:
        self.ships = []
        self.sea_cells = dict()
        for irow in range(RANK):
            for icol in range(RANK):
                one_cell = tuple([irow, icol])
                self.sea_cells[one_cell] = "~"
        self.ships_allocate()

    def allocate_on_seafield(self, nose: tuple, tail: tuple) -> None:
        nose_x = nose[0]
        nose_y = nose[1]
        tail_x = tail[0]
        tail_y = tail[1]
        for i in range(nose_x, tail_x + 1):
            for j_index in range(nose_y, tail_y + 1):
                self.sea_cells[(i, j_index)] = alive_deck

    def ships_allocate(self) -> None:
        for ship_size in range(4, 0, -1):
            for _ in range(5 - ship_size):
                self.allocate_one_ship(ship_size)

    def allocate_one_ship(self, kind_of_ship: int) -> None:
        while True:
            nose_x = randint(0, RANK - 1)
            nose_y = randint(0, RANK - 1)
            choose_direction = choice(directions)
            nose = (nose_x, nose_y,)
            tail = self.calculate_tail(nose_x,
                                       nose_y,
                                       choose_direction,
                                       kind_of_ship)

            if self.verification_passed(nose, tail):
                new_ship = Ship(nose, tail, False)
                self.ships.append(new_ship)
                self.allocate_on_seafield(nose, tail)
                return

    def verification_passed(self, nose: tuple, tail: tuple) -> bool:
        # within sea_field
        # not too close to another ship

        if not (0 <= nose[0] <= RANK - 1):
            return False
        if not (0 <= nose[1] <= RANK - 1):
            return False
        if not (0 <= tail[0] <= RANK - 1):
            return False
        if not (0 <= tail[1] <= RANK - 1):
            return False

        starting_x = nose[0] - 1
        starting_x = max(starting_x, 0)
        starting_y = nose[1] - 1
        starting_y = max(starting_y, 0)
        ending_x = tail[0] + 1
        ending_x = min(ending_x, RANK - 1)
        ending_y = tail[1] + 1
        ending_y = min(ending_y, RANK - 1)

        for i in range(starting_x, ending_x + 1):
            for j_index in range(starting_y, ending_y + 1):
                if self.sea_cells[(i, j_index)] == alive_deck:
                    return False
        return True

    def calculate_tail(self,
                       nose_x: int,
                       nose_y: int,
                       choose_direction: str,
                       kind_of_ship: int) -> tuple | None:

        tail_x = nose_x
        tail_y = nose_y
        # if choose_direction == "n":
        #     tail_x -= kind_of_ship - 1
        if choose_direction == "s":
            tail_x += kind_of_ship - 1
        elif choose_direction == "e":
            tail_y += kind_of_ship - 1
        # elif choose_direction == "w":
        #     tail_y -= kind_of_ship - 1
        return (tail_x, tail_y,)

    def print_seafield(self) -> None:
        for i in range(RANK):
            self.print_one_row(i)

    def print_one_row(self, i: int) -> None:
        for j_index in range(RANK):
            print(self.sea_cells[tuple([i, j_index])], end=" ")
        print("\n")
