import types
from typing import List, Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        if self.is_alive:
            return " \u25A1 "
        else:
            return " * "

    def __repr__(self) -> str:
        if self.is_alive:
            return " \u25A1 "
        else:
            return " * "


def generate_coordinates(
    point1: tuple, point2: tuple, step: int = 1
) -> List[tuple]:
    x1, y1 = point1
    x2, y2 = point2
    coordinates = []

    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1, step):  # noqa: VNE001
            coordinates.append((x1, y))
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1, step):  # noqa: VNE001
            coordinates.append((x, y1))
    else:
        # Calculate slope and intercept of the line
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        for x in range(min(x1, x2), max(x1, x2) + 1, step):  # noqa: VNE001
            y = slope * x + intercept  # noqa: VNE001
            coordinates.append((x, round(y)))

    return coordinates


def create_decks(start: tuple, end: tuple) -> List[Deck]:
    decks = []
    for coord in generate_coordinates(start, end):
        decks.append(Deck(*coord))
    return decks


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = create_decks(start, end)
        self.alive_decks = len(self.decks)

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        deck.is_alive = False
        self.alive_decks -= 1
        if self.alive_decks == 0:
            self.is_drowned = True
            self.change_deck_str()
            return "Sunk!"
        else:
            return "Hit!"

    def change_deck_str(self) -> None:
        def new_str(deck: Any) -> str:
            if deck.is_alive:
                return " \u25A1 "
            else:
                return " x "

        for deck in self.decks:
            deck.__str__ = types.MethodType(new_str, deck)


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship
        self._validate_field()

    def _validate_field(self) -> None:
        validator_dict = {1: 4, 2: 3, 3: 2, 4: 1, "total": 10}
        current_validator_dict = {1: 0, 2: 0, 3: 0, 4: 0, "total": 0}

        for ship in self.ships:
            current_validator_dict[len(ship.decks)] += 1
            current_validator_dict["total"] += 1

        if current_validator_dict != validator_dict:
            raise ValueError("Invalid field!")

    def fire(self, location: tuple) -> str | None:
        if location in self.field:
            ship = self.field[location]
            if not ship.is_drowned:
                return ship.fire(*location)
            return "Already sunk!"
        return "Miss!"

    @staticmethod
    def print_field(field: dict) -> None:
        initial_field = [[" ~ "] * 10 for _ in range(10)]
        for coord, ship in field.items():
            initial_field[coord[0]][coord[1]] = ship.get_deck(
                coord[0], coord[1]
            ).__str__()
        for row in initial_field:
            print(row)
