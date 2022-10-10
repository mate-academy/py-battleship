from __future__ import annotations


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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.len_ship = round(((start[0] - end[0]
                                )**2 + (start[1] - end[1])**2)**0.5) + 1
        self.ship = [Deck(end[0], end[1] - i)
                     if start[1] < end[1]
                     else Deck(end[0] - i, end[1])
                     for i in range(self.len_ship)]
        self.is_drowned = is_drowned

    @staticmethod
    def get_deck(
        boat: Battleship,
        row: int,
        column: int
    ) -> Deck | Ship:

        for ship in boat.boat:
            if not ship.is_drowned:
                for decks in ship.ship:
                    if decks.row == row and decks.column == column:
                        return decks, ship


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:

        self.field = [["~"] * 10 for _ in range(10)]
        self.boat = [Ship(start=coords[0], end=coords[1]) for coords in ships]
        self.take_spot()
        self.check_all_ships_on_field()
        self.check_ship_location_is_correct()

    def take_spot(self) -> None:

        for ship in self.boat:
            for deck in ship.ship:
                self.field[deck.row][deck.column] = "□"
                assert deck.row in range(10) and deck.column in range(10),\
                    "row and column number should be in range 0 to 9"

    def print_field(self) -> None:
        print(*self.field, sep="\n")

    def start_fire(
        self,
        row: int,
        column: int
    ) -> str:

        deck, ship = Ship.get_deck(self, row, column)
        deck.is_alive = False
        ship.len_ship -= 1
        if ship.len_ship == 0:
            ship.is_drowned = True
            self.ship_drowned(ship.ship)
            return "Sunk!"
        return "Hit!"

    def ship_drowned(
            self,
            ship: list
    ) -> None:

        for deck in ship:
            self.field[deck.row][deck.column] = "x"

    def fire(
        self,
        location: tuple
    ) -> str:

        if self.field[location[0]][location[1]] == "□":
            self.field[location[0]][location[1]] = "*"
            return self.start_fire(location[0], location[1])

        return "Miss!"

    def check_ship_location_is_correct(self) -> None:
        for ship in self.boat:
            for another_ship in self.boat:
                if ship != another_ship:
                    for deck in ship.ship:
                        for another_deck in another_ship.ship:
                            if deck.row in range(
                                    another_deck.row - 1,
                                    another_deck.row + 2
                            ) and deck.column in range(
                                    another_deck.column - 1,
                                    another_deck.column + 2
                            ):
                                raise ValueError(
                                    "Ship must be at least 1 "
                                    "position away from the other ship"
                                )

    def check_all_ships_on_field(self) -> None:
        must_have = {
            1: 4,
            2: 3,
            3: 2,
            4: 1
        }
        we_have = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        for ship in self.boat:
            we_have[ship.len_ship] += 1

        assert must_have == we_have, \
            "We need 1 four-deck ship, 2 three-deck boat, " \
            "3 double-deck boat and 4 single-deck boat"
