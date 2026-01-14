"""Contains the core logic of the application."""
from app.ship import Blueprint, Deck, Point, Ship


class Battleship:
    """A class to represent the game."""

    rows_count: int = 10
    columns_count: int = 10

    def __init__(self, ships: list[Blueprint]) -> None:
        """
        Construct all the necessary attributes for the game object.

        :param ships: a list of ships to be placed on the field
        """
        self.field = ships

    @property
    def field(self) -> dict[Blueprint, Ship]:
        """Get the field of the game."""
        return self.__field

    @field.setter
    def field(self, ships: list[Blueprint]) -> None:
        self.__field = dict()
        for blueprint in ships:
            self._validate_points(*blueprint)
            self.__field[blueprint] = Ship(self._shipyard(blueprint))
        self._validate_field()

    def _validate_points(self, *points: Point) -> None:
        """
        Validate the points.

        :param points: a list of points to be validated
        :raises TypeError: if the point contains non-integer value
        :raises ValueError: if the point is out of field range
        """
        for row, column in points:
            if not isinstance(row, int) or not isinstance(column, int):
                raise TypeError(
                    f"The coordinate: {(row, column)} "
                    + "contains noninteger value!"
                )
            if (
                not 0 <= row < self.rows_count
                or not 0 <= column < self.columns_count
            ):
                raise ValueError(
                    f"The coordinate: {(row, column)} is out of field range!"
                )

    @staticmethod
    def _shipyard(blueprint: Blueprint) -> list[Point]:
        """
        Build the ship from the blueprint.

        :param blueprint: a blueprint of the ship
        :return: a list of points of the ship
        """
        for i in range(2):
            if (locked := blueprint[0][i]) == blueprint[1][i]:
                axis = abs(i - 1)
                start, end = sorted(
                    (blueprint[0][axis], blueprint[1][axis])
                )
                return [
                    (locked, coord) if i == 0 else (coord, locked)
                    for coord in range(start, end + 1)
                ]
        raise ValueError(
            "The shipyard can built only straight, "
            + "vertical or horizontal ships!"
        )

    def _validate_field(self) -> None:
        """
        Validate the field.

        :raises ValueError: if the fleet is invalid
        """
        ships = list(self.field.values())
        if len(ships) != 10:
            raise ValueError("The fleet must consist of 10 ships!")

        ships_amount = {
            1: 4,
            2: 3,
            3: 2,
            4: 1,
        }
        for ship in ships:
            ships_amount[len(ship.hull_sections)] -= 1

        if any(amount != 0 for amount in ships_amount.values()):
            raise ValueError("Invalid fleet composition!")

        for ship in ships:
            for deck in ship.hull_sections:
                row, col = deck.position
                for neighbor in [
                    (row + dr, col + dc)
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                ]:
                    if (
                        self._get_field_point(*neighbor)
                        and neighbor not in (
                            d.position
                            for d in ship.hull_sections
                        )
                    ):
                        raise ValueError(
                            "Ship touches or "
                            + f"intersects another at {neighbor}!"
                        )

    def _get_field_point(
            self,
            row: int,
            column: int,
            only_ship: bool = False
    ) -> Deck | Ship | None:
        """
        Get the point of the field.

        :param row: a row of the point
        :param column: a column of the point
        :param only_ship: a flag to get only the ship
        :return: a deck or a ship or None
        """
        for ship in self.field.values():
            if (row, column) in (deck.position for deck in ship.hull_sections):
                return ship if only_ship else ship.get_deck(row, column)
        return None

    def fire(self, location: Point) -> str:
        """
        Fire at the location.

        :param location: a location to fire
        :return: a message about the result of the fire
        """
        self._validate_points(location)
        if ship := self._get_field_point(*location, only_ship=True):
            if ship.fire(*location):
                if ship.is_drowned:
                    return "Sunk!"

                return "Hit!"

        return "Miss!"

    def is_fleet_drowned(self) -> bool:
        """
        Check if the fleet is drowned.

        :return: True if the fleet is drowned, False otherwise
        """
        return all(ship.is_drowned for ship in self.field.values())

    def print_field(self) -> None:
        """Print the field."""
        for row in range(self.rows_count):
            render_row = list()
            for column in range(self.columns_count):
                if deck := self._get_field_point(row, column):
                    if deck.ship.is_drowned:
                        render_row.append("x")
                    elif deck.is_alive:
                        render_row.append(u"\u25A1")
                    else:
                        render_row.append("*")
                else:
                    render_row.append("~")

            print(*render_row)
