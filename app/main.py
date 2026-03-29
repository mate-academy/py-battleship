from app.custom_exeptions import (
    ShipCreationError,
    NominalShipError,
    WrongCoordinatesError,
    CanNotBeNeighbourError
)


class Deck:
    """Creates Deck with row, column parameters
    is_alive, while the deck was not on fire
    """

    def __init__(
            self,
            row: int = 9,
            column: int = 9,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Row: {self.row}, Column: {self.column}"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        """Create decks and save them to a list `self.decks`"""
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))
        elif self.start[1] < self.end[1]:
            temp = self.start[1]
            while temp <= self.end[1]:
                self.decks.append(Deck(self.start[0], temp))
                temp += 1
        elif self.start[0] < self.end[0]:
            temp = self.start[0]
            while temp <= self.end[0]:
                self.decks.append(Deck(temp, self.start[1]))
                temp += 1
        else:
            raise WrongCoordinatesError

    def __str__(self) -> str:
        return f"Ship: {self.decks}"

    def get_deck(self, row: int, column: int) -> Deck:
        """
        Return Deck if deck with "row" and "column" in ship,
        else return None
        """
        return next(
            (deck for deck in self.decks
             if deck.row == row and deck.column == column),
            None)

    def fire(self, row: int, column: int) -> None:
        """
        Change the `is_alive` status of the deck
        And update the `is_drowned` value if it's needed
        """
        deck_on_fire = self.get_deck(row=row, column=column)
        if deck_on_fire:
            deck_on_fire.is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        """
        Creates a dict `self.field`.
        Its keys are tuples - the coordinates of the non-empty cells,
        A value for each cell is a reference to the ship
        which is located in it
        """
        self._validate_ships_list(ships)
        self.field = {}
        for start in range(0, 10):
            for end in range(0, 10):
                self.field[(start, end)] = None
        for coordinates in ships:
            ship = Ship(coordinates[0], coordinates[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self.ships_location_validation()

    def fire(self, location: tuple) -> str:
        """
        This function checks whether the location
        is a key in the `self.field`
        If it is, then it checks if this cell is the last alive
        in the ship or not.
        It returns string with result
        """
        ship_on_fire = self.field.get(location)
        if ship_on_fire:
            ship_on_fire.fire(location[0], location[1])
            if ship_on_fire.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> str:
        """
        Prints field:
        - no ship = "----"
        - alive ships deck = "DECK"
        - fired ships deck = "BOOM"
        """
        representation = ""
        for key, value in self.field.items():
            if value:
                if value.get_deck(key[0], key[1]).is_alive:
                    representation += "DECK "
                elif not value.get_deck(key[0], key[1]).is_alive:
                    representation += "BOOM "
            else:
                representation += "---- "
            if key[1] == 9:
                representation += "\n"
        return representation

    def _validate_ships_list(self, ships: list[tuple]) -> None:
        """
        Validate the ships list:
        - the total number of the ships should be 10;
        - there should be 4 single-deck ships;
        - there should be 3 double-deck ships;
        - there should be 2 three-deck ships;
        - there should be 1 four-deck ship;
        """
        if len(ships) != 10:
            raise ShipCreationError
        self.ships_nominal_validation(ships=ships)

    @staticmethod
    def ships_nominal_validation(ships: list[tuple]) -> None:
        """
        Checking, if list of coordinates for creating field has
        correct nominal of ships
        """
        ships_count_dict = {
            "one_deck": 0,
            "two_decks": 0,
            "three_decks": 0,
            "four_decks": 0
        }
        for ship in ships:
            if ship[0] == ship[1]:
                ships_count_dict["one_deck"] += 1
            elif sum(ship[0]) == sum(ship[1]) - 1:
                ships_count_dict["two_decks"] += 1
            elif sum(ship[0]) == sum(ship[1]) - 2:
                ships_count_dict["three_decks"] += 1
            elif sum(ship[0]) == sum(ship[1]) - 3:
                ships_count_dict["four_decks"] += 1

        correct_ships_dict = {
            "one_deck": 4,
            "two_decks": 3,
            "three_decks": 2,
            "four_decks": 1
        }
        if ships_count_dict != correct_ships_dict:
            raise NominalShipError

    def ships_location_validation(self) -> None:
        """
        Checking, if ships, that was created are
         not located in the neighboring cells
        """
        for key, value in self.field.items():
            if value:
                round_list = [
                    (key[0] - 1, key[1] - 1),
                    (key[0] - 1, key[1]),
                    (key[0] - 1, key[1] + 1),
                    (key[0], key[1] - 1),
                    (key[0], key[1] + 1),
                    (key[0] + 1, key[1] - 1),
                    (key[0] + 1, key[1]),
                    (key[0] + 1, key[1] + 1),
                ]
                for item in round_list:
                    if (self.field.get(item)
                            and self.field.get(item) != self.field.get(key)):
                        raise CanNotBeNeighbourError
