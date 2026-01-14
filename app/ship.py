"""Module with builders for ships and their components."""
Point = tuple[int, int]
Blueprint = tuple[Point, Point]


class Deck:
    """A class to represent a single ship`s deck."""

    def __init__(
            self,
            row: int,
            column: int,
            ship: "Ship",
            is_alive: bool = True
    ) -> None:
        """
        Construct all the necessary attributes for the deck object.

        :param row: a row of the deck
        :param column: a column of the deck
        :param ship: a ship the deck belongs to
        :param is_alive: a status of the deck
        """
        self.position = row, column
        self.ship = ship
        self.is_alive = is_alive

    @property
    def position(self) -> Point:
        """Get the position of the deck."""
        return self.__row, self.__column

    @position.setter
    def position(self, point: Point) -> None:
        self.__row, self.__column = point

    @property
    def is_alive(self) -> bool:
        """Get the status of the deck."""
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError("A deck can be only alive or hit!")

        self.__is_alive = status


class Ship:
    """A class to represent a single ship."""

    def __init__(self, ship: list[Point], is_drowned: bool = False) -> None:
        """
        Construct all the necessary attributes for the ship object.

        :param ship: a list of points of the ship
        :param is_drowned: a status of the ship
        """
        self.hull_sections = ship
        self.is_drowned = is_drowned

    @property
    def hull_sections(self) -> list[Deck]:
        """Get the hull sections of the ship."""
        return self.__hull_sections

    @hull_sections.setter
    def hull_sections(self, ship: list[Point]) -> None:
        self.__hull_sections = [Deck(*point, ship=self) for point in ship]

    @property
    def is_drowned(self) -> bool:
        """Get the status of the ship."""
        return self.__is_drowned

    @is_drowned.setter
    def is_drowned(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError("A ship can be only afloat or drowned!")

        self.__is_drowned = status

    def get_deck(self, row: int, column: int) -> Deck | None:
        """
        Get the deck of the ship by its position.

        :param row: a row of the deck
        :param column: a column of the deck
        :return: a deck of the ship or None
        """
        for deck in self.hull_sections:
            if deck.position == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        """
        Fire at the ship.

        :param row: a row to fire
        :param column: a column to fire
        :return: True if the ship was hit, False otherwise
        """
        if (deck := self.get_deck(row, column)) and deck.is_alive:
            deck.is_alive = False

            if not any(deck.is_alive for deck in self.hull_sections):
                self.is_drowned = True

            return True
        return False
