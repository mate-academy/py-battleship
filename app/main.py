from __future__ import annotations


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

    @staticmethod
    def create_deck(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[Deck]:
        decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(row, column))
        return decks


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = Deck.create_deck(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError("Deck was not found")

    def get_decks(self) -> tuple:
        dec = []
        for deck in self.decks:
            dec.append((deck.row, deck.column))
        return tuple(dec)

    def is_ship_alive(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return True
        return False

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not self.is_ship_alive():
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        fields = {}
        for ship_ends in ships:
            ship = Ship(ship_ends[0], ship_ends[1])
            fields[ship.get_decks()] = ship
        self.field = fields

    @property
    def field(self) -> dict:
        return self._field

    @field.setter
    def field(self, ships: dict[tuple]) -> None:
        Battleship._validate_field(ships)
        self._field = ships

    @staticmethod
    def get_ship(decs_and_ships: dict, location: tuple) -> Ship | None:
        for cells, ship in decs_and_ships.items():
            if location in cells:
                return ship

    def fire(self, location: tuple) -> str:
        ship = Battleship.get_ship(self.field, location)
        if not ship:
            return "Miss!"
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = Battleship.get_ship(self.field, (row, column))
                if not ship:
                    print("~", end="")
                elif ship.is_drowned:
                    print("x", end="")
                elif ship.get_deck(row, column).is_alive:
                    print("□", end="")
                else:
                    print("x", end="")
            print()

    @staticmethod
    def _validate_field(ships: dict[tuple]) -> None:
        if len(ships) != 10:
            raise ValueError("Should be 10 ships")
        ships_counter = [0] * 4
        for ship in ships:
            if len(ship) > 4:
                raise ValueError("More than needed decks")
            ships_counter[len(ship) - 1] += 1
            if Battleship.check_if_ship_located_in_neighboring_cells(
                    ships, ship
            ):
                raise ValueError("Ships located in neighboring cells")
        for i in range(len(ships_counter)):
            if 4 - i != ships_counter[i]:
                raise ValueError(f"Should be {i + 1} {4 - i}-deck ships")

    @staticmethod
    def check_if_ship_located_in_neighboring_cells(
            ships: dict[tuple],
            ship_to_check: tuple
    ) -> bool:
        for location in ship_to_check:
            for row in range(-1, 2):
                if row == -1 and location[0] == 0:
                    continue
                for column in range(-1, 2):
                    if column == -1 and location[1] == 0:
                        continue
                    found_ship = Battleship.get_ship(
                        ships,
                        (location[0] + row, location[1] + column)
                    )
                    if found_ship and ship_to_check != found_ship.get_decks():
                        return True
        return False
