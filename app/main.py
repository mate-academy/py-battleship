from typing import List, Tuple, Dict


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: int = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.decks: List[Deck] = []

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

        self.is_drowned: bool = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        dead_deck = self.get_deck(row, column)
        dead_deck.is_alive = False

        is_at_least_one_deck_alive: bool = False

        for deck in self.decks:
            if deck.is_alive:
                is_at_least_one_deck_alive = True

        if not is_at_least_one_deck_alive:
            self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple, Ship] = {}
        self.ship_and_num_of_decks: Dict[Ship, int] = {}

        for ship_cord in ships:
            ship = Ship(ship_cord[0], ship_cord[1])
            self.ship_and_num_of_decks[ship] = 0

            for row in range(ship_cord[0][0], ship_cord[1][0] + 1):
                for column in range(ship_cord[0][1], ship_cord[1][1] + 1):
                    self.field[(row, column)] = ship
                    self.ship_and_num_of_decks[ship] += 1

        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            else:
                return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for column in range(0, 10):
                if (row, column) not in self.field:
                    print("~", end="")
                elif self.field[(row, column)].is_drowned:
                    print("x", end="")
                elif self.field[(row, column)]\
                        .get_deck(row, column).is_alive:
                    print("#", end="")
                else:
                    print("*", end="")

                print(" ", end="")
            print("")
        print("")

    def _validate_field(self) -> None:
        self._correct_number_of_ships(10)
        self._correct_number_of_decks({
            1: 4,
            2: 3,
            3: 2,
            4: 1
        })
        self._validate_neighboring_cells_of_ships()

    def _validate_neighboring_cells_of_ships(self) -> None:
        for location, ship in self.field.items():
            assert not self._is_there_another_ship_nearby(location, ship),\
                "Two ships next to each other"

    def _is_there_another_ship_nearby(
        self,
        location: Tuple[int, int],
        this_ship: Ship
    ) -> bool:
        for row in range(-1, 2):
            for column in range(-1, 2):
                checking_location = (
                    location[0] + row,
                    location[1] + column
                )

                if checking_location not in self.field:
                    continue

                if self.field[checking_location] is not this_ship:
                    return True

        return False

    def _correct_number_of_ships(
        self,
        correct_number: int
    ) -> None:
        assert len(self.ship_and_num_of_decks) == correct_number, \
            "There should be 10 ships"

    def _correct_number_of_decks(
        self,
        correct_setup: Dict[int, int]
    ) -> None:
        ships_with_num_of_decks: Dict[int, int] = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        for decks_in_ship in self.ship_and_num_of_decks.values():
            ships_with_num_of_decks[decks_in_ship] += 1

        assert ships_with_num_of_decks == correct_setup, \
            "Wrong number of decks in ship"
