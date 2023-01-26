from typing import List, Dict, Tuple


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

        self.is_drowned = is_drowned

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
        self.field = {}
        self.ship_and_num_of_decks = {}

        for ship_cord in ships:
            ship = Ship(ship_cord[0], ship_cord[1])
            self.ship_and_num_of_decks[ship] = 0

            for row in range(ship_cord[0][0], ship_cord[1][0] + 1):
                for column in range(ship_cord[0][1], ship_cord[1][1] + 1):
                    self.field[(row, column)] = ship
                    self.ship_and_num_of_decks[ship] += 1

        self._validating_field()

    def fire(self, coordinates: Tuple[int, int]) -> str:
        if coordinates in self.field:
            self.field[coordinates].fire(*coordinates)
            if self.field[coordinates].is_drowned:
                return "Sunk!"
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
                print("*", end="")

                print(" ", end="")
            print("")
        print("")

    def _validating_field(self) -> None:
        assert len(self.ship_and_num_of_decks) == 10, \
            "There should be 10 ships"
        self._validating_amount_of_decks({
            1: 4,
            2: 3,
            3: 2,
            4: 1
        })
        for coordinates, ship in self.field.items():
            assert not self._is_there_another_ship_nearby(coordinates, ship), \
                "Two ships next to each other"

    def _is_there_another_ship_nearby(
        self,
        coordinates: Tuple[int, int],
        this_ship: Ship
    ) -> bool:
        for row in range(-1, 2):
            for column in range(-1, 2):
                checking_coordinates = (
                    coordinates[0] + row,
                    coordinates[1] + column
                )

                if checking_coordinates not in self.field:
                    continue

                if self.field[checking_coordinates] is not this_ship:
                    return True

        return False

    def _validating_amount_of_decks(
        self,
        correct_setup: Dict[int, int]
    ) -> None:
        ships_with_num_of_decks = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        for decks_in_ship in self.ship_and_num_of_decks.values():
            ships_with_num_of_decks[decks_in_ship] += 1

        assert ships_with_num_of_decks == correct_setup, \
            "Wrong number of decks in ship"
