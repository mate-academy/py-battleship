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
    def validate_amount_of_ships(cls) -> bool:
        for ship_size, count in cls.ships_amount.items():
            if ship_size + count != 5:
                raise ShipAmountError("The number of ships is incorrect")
        return True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self._validate_ship_diagonal(ship)
            new_ship = Ship(ship[0], ship[1])
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

    def _validate_location(self, location: tuple) -> bool:
        if location[0] in range(10) and location[1] in range(10):
            return True
        raise LocationError(f"Provided location {location} is "
                            "out of available range")

    def _validate_ship_diagonal(self, ship_location: tuple) -> bool:
        ship_start = ship_location[0]
        ship_end = ship_location[1]
        self._validate_location(ship_start)
        self._validate_location(ship_end)
        if ship_start[0] != ship_end[0] and ship_start[1] != ship_end[1]:
            raise ShipPlacementError("Ships can't be placed on a diagonal")
        return True

    def _validate_ship_collision(self, ships: list[tuple]) -> bool:
        for index, ship in enumerate(ships):
            for current_point in ship:
                for compare_ship_index in range(index + 1, 10):
                    for check_ship_point in ships[compare_ship_index]:
                        first_diff = abs(
                            current_point[0] - check_ship_point[0]
                        )
                        second_diff = abs(
                            current_point[1] - check_ship_point[1]
                        )
                        diff_sum = sum((first_diff, second_diff))
                        if diff_sum < 2:
                            raise ShipCollisionError("Ship collision detected")
                        if diff_sum == 2:
                            if first_diff == 1 or second_diff == 1:
                                raise ShipCollisionError("Ship collision "
                                                         "detected")
