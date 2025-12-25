from dataclasses import dataclass


@dataclass
class Deck:
    """Represents one deck (cell) of a ship:
    contains its coordinates and alive/dead state."""

    row: int
    column: int
    is_alive: bool = True


class Ship:
    """
    Represents a ship defined by two endpoints (start, end).
    Builds its Deck objects, can be hit, and can become fully sunk.
    """

    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        """
        :param start: tuple(int, int) - coordinates of the first deck
        :param end: tuple(int, int) - coordinates of the last deck
        :param is_drowned: bool - status flag,
        becomes True when all decks are dead
        """
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        (row_1, col_1), (row_2, col_2) = start, end

        if row_1 == row_2:
            for column in range(min(col_1, col_2), max(col_1, col_2) + 1):
                self.decks.append(Deck(row_1, column))
        else:
            for row in range(min(row_1, row_2), max(row_1, row_2) + 1):
                self.decks.append(Deck(row, col_1))

    def get_deck(self, row: int, column: int) -> None | Deck:
        """Returns the deck at the given coordinates,
        or None if not part of this ship."""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return

    def fire(self, row: int, column: int) -> str | None:
        """
        Processes a shot at this ship.
        Marks deck dead if hit and returns:
        "Hit!" if ship still has alive decks,
        "Sunk!" if it was the last deck.
        """
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return


class Battleship:
    """
    Game engine for Battleship.
    Responsible for field setup, validating fleet rules,
    handling shots, and displaying the board.
    """

    def __init__(self, ships: list[tuple[int]]) -> None:
        """
        :param ships: list of tuples ((r1,c1),(r2,c2))
        Builds all ships and maps each coordinate to its ship.
        """
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str | None:
        """
        Fires at a given (row, col) location.
        Returns "Miss!", "Hit!" or "Sunk!".
        """
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(*location)

    def print_field(self) -> None:
        """Prints 10x10 board showing ships and hit/miss states."""

        board = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    board[deck.row][deck.column] = "□"
                else:
                    board[deck.row][deck.column] = "x" \
                        if ship.is_drowned else "*"

        for row in board:
            print(" ".join(row))
        print()

    def _validate_field(self) -> None:
        """Ensures correct ship count and prevents ships from touching."""

        assert len(self.ships) == 10, "Total ships must be 10"

        ship_lengths = {}
        for ship in self.ships:
            length = len(ship.decks)
            ship_lengths[length] = ship_lengths.get(length, 0) + 1

        assert ship_lengths.get(1, 0) == 4, "4 single-deck ships required"
        assert ship_lengths.get(2, 0) == 3, "3 double-deck ships required"
        assert ship_lengths.get(3, 0) == 2, "2 triple-deck ships required"
        assert ship_lengths.get(4, 0) == 1, "1 four-deck ship required"

        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]

        for (row, col), ship in self.field.items():
            for dr, dc in directions:
                neighbor = (row + dr, col + dc)
                if (neighbor in self.field
                        and self.field[neighbor] != ship):
                    raise ValueError("Ships cannot touch "
                                     "— adjacency violation!")
