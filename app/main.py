from itertools import combinations
from typing import Iterator


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        # Create a Deck object - its location and info if it was hit
        self._row = row
        self._column = column
        self._is_alive = is_alive

    @property
    def coordinates(self) -> tuple[int, int]:
        return self._row, self._column

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self._is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self._is_drowned = is_drowned
        if start == end:
            self._decks = [Deck(*start)]
            return
        coordinates = ([], [])
        for i in (0, 1):
            coordinates[i].extend(
                range(start[i], end[i] + 1) if start[i] <= end[i]
                else range(start[i], end[i] + 1, -1)
            )
        if start[0] == end[0]:
            coordinates[0].extend(coordinates[0] * (len(coordinates[1]) - 1))
        elif start[1] == end[1]:
            coordinates[1].extend(coordinates[1] * (len(coordinates[0]) - 1))
        self._decks = [Deck(*pair) for pair in zip(*coordinates)]

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        return next(
            (
                deck for deck in self._decks
                if deck.coordinates == (row, column)
            ),
            None
        )

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck is None:
            return
        deck.is_alive = False
        if all(deck.is_alive is False for deck in self._decks):
            self._is_drowned = True

    @property
    def length(self) -> int:
        return len(self._decks)

    @property
    def decks(self) -> Iterator[Deck]:
        return iter(self._decks)

    @property
    def is_drowned(self) -> bool:
        return self._is_drowned


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self._field = {}
        for ship in ships:
            ship_object = Ship(*ship)
            for deck in ship_object.decks:
                self._field[deck.coordinates] = ship_object
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self._field:
            return "Miss!"
        self._field[location].fire(*location)
        if self._field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                (
                    print(" x", end="")
                    if self._field[(row, col)].is_drowned
                    else (
                        print(u" \u25A1", end="")
                        if self._field[(row, col)].get_deck(row, col).is_alive
                        else print(" *", end="")
                    )
                ) if (row, col) in self._field else print(" ~", end="")
            print("\n", end="")

    @property
    def ships(self) -> set[Ship]:
        return set(self._field.values())

    @property
    def field(self) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
        # for future usage
        return iter(self._field)

    def _ships_quantity(self, ship_length: int = None) -> int:
        return sum(
            map(lambda ship: ship.length == ship_length, self.ships)
        ) if ship_length else len(self.ships)

    def _any_neighbouring_ships(self) -> bool:
        for cell1, cell2 in combinations(self._field, 2):
            if all(abs(x1 - x2) <= 1 for x1, x2 in zip(cell1, cell2)) and (
                    self._field[cell1] is not self._field[cell2]
            ):
                return True
        return False

    def _validate_field(self) -> None:
        ships_required_quantity = {1: 4, 2: 3, 3: 2, 4: 1}
        error_flag = False
        error_message = []
        if self._ships_quantity() != sum(ships_required_quantity.values()):
            error_message.append("Wrong overall amount of ships!")
            error_flag = True
        for length in ships_required_quantity:
            if self._ships_quantity(length) != ships_required_quantity[length]:
                error_message.append(f"Wrong amount of {length}-deck ships!")
                error_flag = True
        if self._any_neighbouring_ships():
            error_message.append("Ships too close to each other!")
            error_flag = True
        if error_flag:
            raise ValueError(" ".join(error_message))
