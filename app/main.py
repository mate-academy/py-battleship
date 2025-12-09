from typing import List, Tuple, Dict


class Deck:
    """Represents a single deck of a ship in the Battleship game."""

    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        """
        Args:
            row (int): The row coordinate of the deck.
            column (int): The column coordinate of the deck.
            is_alive (bool, optional): Whether the deck is still alive.
            Defaults to True.
        """
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    """Represents a ship composed of multiple decks."""

    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int]) -> None:
        """
        Initialize a ship with its start and end coordinates.

        Args:
            start (Tuple[int, int]): Coordinates of one end of the ship
                (row, col).
            end (Tuple[int, int]): Coordinates of the other end of the
                ship (row, col).

        Raises:
            ValueError: If the ship is not placed horizontally or vertically.
        """
        self.decks: List[Deck] = []

        row1, column1 = start
        row2, column2 = end

        if row1 == row2:
            for column in range(min(column1, column2),
                                max(column1, column2) + 1):
                self.decks.append(Deck(row1, column))
        elif column1 == column2:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, column1))
        else:
            raise ValueError("Ships must be placed horizontally or vertically")

    def get_deck(self, row: int, column: int) -> Deck | None:
        """Return the deck at the specified coordinates.

        Args:
            row (int): Row coordinate of the deck.
            column (int): Column coordinate of the deck.

        Returns:
            Deck | None: The Deck object if found, otherwise None.
        """
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        """Registers a shot at the ship at the given coordinates.

        Args:
            row (int): Row coordinate of the shot.
            column (int): Column coordinate of the shot.

        Returns:
            str: "Miss!" if no deck exists there, "Hit!" if ship is hit
            but not sunk, "Sunk!" if the shot sinks the ship.
        """
        deck = self.get_deck(row, column)
        if not deck:
            return "Miss!"

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            return "Sunk!"
        return "Hit!"


class Battleship:
    """Represents the Battleship game field and manages ships and shots."""

    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
                 ) -> None:
        """
        Initialize the game field with ships.

        Args:
            ships (List[Tuple[Tuple[int, int], Tuple[int, int]]]):
                A list of ships represented by tuples of start
                and end coordinates.
        """
        self.field: Dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        """Registers a shot at the given location on the field.

        Args:
            location (Tuple[int, int]): Coordinates (row, column) to fire at.

        Returns:
            str: "Miss!" if no ship is at location, "Hit!" if ship is hit,
            "Sunk!" if ship is sunk.
        """
        if location not in self.field:
            return "Miss!"

        row, col = location
        ship = self.field[location]

        return ship.fire(row, col)
