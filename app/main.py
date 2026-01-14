from typing import Any


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


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(start[0] if start[0] == end[0] else row,
                 start[1] if start[1] == end[1] else col)
            for row in range(start[0], end[0] + 1)
            for col in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.check_drowned()

    def check_drowned(self) -> None:
        alive_decks = [deck.is_alive for deck in self.decks]
        self.is_drowned = not any(alive_decks)


class Battleship:
    def __init__(self, ships: list[tuple, tuple]) -> None:
        self.field = {}
        self.ships = []
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def _validate_field(self) -> None:
        ships_count = len(self.ships)
        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            decks_count = len(ship.decks)
            if decks_count in counts:
                counts[decks_count] += 1

        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}

        if ships_count != 10 or counts != expected_counts:
            raise ValueError

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, col)
                    if not deck.is_alive:
                        if ship.is_drowned:
                            print("x", end=" ")
                        else:
                            print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()
