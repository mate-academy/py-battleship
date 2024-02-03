from itertools import product


class LocationError(Exception):
    pass


class ShipError(Exception):
    pass


class ShipPlacementError(ShipError):
    pass


class ShipAmountError(ShipError):
    pass


class ShipCollisionError(ShipError):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    ships_amount = {ship_size: 0 for ship_size in range(1, 5)}

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column) for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.ships_amount[len(self.decks)] += 1

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True

    @classmethod
    def validate_amount_of_ships(cls) -> None:
        for ship_size, count in cls.ships_amount.items():
            if ship_size + count != 5:
                raise ShipAmountError("The number of ships is incorrect")


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self._validate_ship_diagonal(ship)
            new_ship = Ship(*ship)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        Ship.validate_amount_of_ships()
        self._validate_ship_collision(ships)

    def fire(self, location: tuple) -> str:
        self._validate_location(location)
        if self.field.get(location):
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for column in range(10):
                if (row, column) in self.field:
                    current_ship = self.field[(row, column)]
                    current_deck = current_ship.get_deck(row, column)
                    if current_deck.is_alive:
                        row_str += u"\u25A1"
                    elif current_ship.is_drowned:
                        row_str += "x"
                    else:
                        row_str += "*"
                    continue
                row_str += "~"
            print(row_str)

    def _validate_location(self, location: tuple) -> None:
        if location[0] not in range(10) or location[1] not in range(10):
            raise LocationError(f"Provided location {location} is "
                                "out of available range")

    def _validate_ship_diagonal(self, ship_location: tuple) -> None:
        ship_start = ship_location[0]
        ship_end = ship_location[1]
        self._validate_location(ship_start)
        self._validate_location(ship_end)
        if ship_start[0] != ship_end[0] and ship_start[1] != ship_end[1]:
            raise ShipPlacementError("Ships can't be placed on a diagonal")

    def _validate_ship_collision(self, ships: list[tuple]) -> None:
        for first_ship, second_ship in product(ships, repeat=2):
            print(first_ship, second_ship)
            if first_ship is not second_ship:
                if any(self.__collision_detected(first_point, second_point)
                       for first_point in first_ship
                       for second_point in second_ship):
                    raise ShipCollisionError("Ship collision detected")

    def __collision_detected(
            self,
            first_point: tuple,
            second_point: tuple
    ) -> bool:
        first_diff = abs(first_point[0] - second_point[0])
        second_diff = abs(first_point[1] - second_point[1])
        return (first_diff + second_diff < 2
                or (first_diff == 1 and second_diff == 1))
