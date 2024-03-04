class WrongShipsNumberError(Exception):
    pass


class LocationError(Exception):
    pass


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

    @classmethod
    def create_ship_decks(
            cls,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list:
        return [
            cls(row=row, column=column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = Deck.create_ship_decks(start, end)

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if (deck.row == row) and (deck.column == column):
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.decks.remove(deck)

        if not self.decks:
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple]
    ) -> None:
        self.ships = ships
        self.field = {}

        ship_list = [Ship(start, end) for start, end in ships]

        self.field = {
            (deck.row, deck.column): ship
            for ship in ship_list
            for deck in ship.decks
        }

        self._validate_field(ship_list)

    def fire(
            self,
            location: tuple[int, int]
    ) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                deck.is_alive = False
                if all(not deck.is_alive for deck in ship.decks):
                    ship.is_drowned = True
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        non_empty_cells = sorted(self.field.keys())
        ship = self.field.get
        for row in range(0, 10):
            for column in range(0, 10):
                if not (row, column) in non_empty_cells:
                    print("~", end="")
                else:
                    if ship((row, column)).is_drowned:
                        print("x", end="")
                    elif ship((row, column)).get_deck(row, column).is_alive:
                        print(u"\u25A1", end="")
                    else:
                        print("*", end="")
                print("\t", end="")
            print("\n", end="")

    def _validate_field(
            self,
            ship_list: list[Ship]
    ) -> None:
        Battleship._check_total_number_of_ships(self)

        ships_decks = [ship.decks for ship in ship_list]
        Battleship._check_ships_with_specific_number_of_decks(ships_decks)

        Battleship._check_ships_neighbor_location(self)

    def _check_total_number_of_ships(self) -> None:
        if len(self.ships) != 10:
            raise WrongShipsNumberError(
                f"{len(self.ships)} ships instead of 10."
            )

    @staticmethod
    def _check_ships_with_specific_number_of_decks(
            ships_decks_list: list[list[Deck]]
    ) -> None:
        length_of_ships = [4, 3, 2, 1]
        expected_counts = [1, 2, 3, 4]

        for ship_len, expected_count in zip(length_of_ships, expected_counts):
            count_decks = len(
                [ship_decks for ship_decks in ships_decks_list
                 if len(ship_decks) == ship_len]
            )
            if count_decks != expected_count:
                raise WrongShipsNumberError(
                    f"{count_decks} {ship_len}-deck ships "
                    f"instead of {expected_count}"
                )

    def _check_ships_neighbor_location(self) -> None:
        for location, ship in self.field.items():
            for neighbor_row in range(location[0] - 1, location[0] + 1):
                for neighbor_column in range(location[1] - 1, location[1] + 1):
                    neighbor_location = (neighbor_row, neighbor_column)

                    if (
                        neighbor_location in self.field
                        and not self.field[neighbor_location] == ship
                    ):
                        raise LocationError(
                            f"{ship} shouldn't be located "
                            f"in the neighboring cells "
                            f"with {self.field[neighbor_location]}!"
                        )
