from typing import List, Tuple, Dict


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

    def get_coord(self) -> tuple:
        return self.row, self.column


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: List[Deck] = self._create_decks()

    def _create_decks(self) -> list:
        return [Deck(row, column)
                for row in range(self.start[0], self.end[0] + 1)
                for column in range(self.start[1], self.end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def size(self) -> int:
        return len(self.decks)

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:

    def __init__(self, ships: List[Tuple[tuple]]) -> None:
        self.limits: dict = {4: 1, 3: 2, 2: 3, 1: 4}
        self.location_ships = set()
        self.field: Dict[Tuple[int, int], Ship] = {}
        self._validate_field(ships)

    def _range_ship(self, ship: Ship) -> None:
        for deck in ship.decks:
            for row in range(deck.row - 1, deck.row + 2):
                for column in range(deck.column - 1, deck.column + 2):
                    if 0 <= row < 10 and 0 <= column < 10:
                        coordinate = (row, column)
                        if coordinate not in self.location_ships:
                            self.location_ships.add(coordinate)

    def _validate_field(self, ships: List[Tuple[Tuple[int, int]]]) -> dict:
        for start, end in ships:
            if start in self.location_ships or end in self.location_ships:
                raise ValueError(
                    f"Ship with that location "
                    f"{(start, end)} can`t be placed!"
                )

            ship = Ship(start, end)
            if not self.limits[ship.size()]:
                raise ValueError(
                    f"There are already enough "
                    f"ships with that size({ship.size()})!"
                )
            self.limits[ship.size()] -= 1
            self._range_ship(ship)
            self.field.update({deck.get_coord(): ship for deck in ship.decks})

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        simbols: dict = {
            "is_not_drowned": "X",
            "is_alive": "*",
            "ship": u"\u25A1",
            "empty": "~"}

        battlefield = [[simbols["empty"]] * 10 for _ in range(0, 10)]
        for location, ships in self.field.items():
            deck = ships.get_deck(*location)
            if ships.is_drowned:
                battlefield[deck.row][deck.column] = simbols["is_not_drowned"]
                continue

            if not deck.is_alive:
                battlefield[deck.row][deck.column] = simbols["is_alive"]
                continue

            battlefield[deck.row][deck.column] = simbols["ship"]

        for field in battlefield:
            print(field)
