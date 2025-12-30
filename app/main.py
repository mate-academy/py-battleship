from typing import Any, Tuple, List, Dict


class Deck:

    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:

        self.decks: List[Deck] = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck or None:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> str:

        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:

        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(
            self,
            location: tuple[Any, Any]
    ) -> str:
        row, column = location
        if location in self.field:
            return self.field[location].fire(row, column)
        else:
            return "Miss!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships.")

        ship_sizes = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            size = len(ship.decks)
            if size in ship_sizes:
                ship_sizes[size] += 1
            else:
                raise ValueError("Invalid ship size found.")

        if (
                ship_sizes[1] != 4
                or ship_sizes[2] != 3
                or ship_sizes[3] != 2
                or ship_sizes[4] != 1
        ):
            raise ValueError("Incorrect distribution of ships by size.")

        for ship in self.ships:
            for deck in ship.decks:
                for drow in range(-1, 2):
                    for dcol in range(-1, 2):
                        neighbor = (
                            deck.row + drow, deck.column + dcol
                        )
                        if (
                                neighbor in self.field
                                and self.field[neighbor] != ship
                        ):
                            raise ValueError("Ships are improperly placed.")

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    deck = self.field[(row, column)].get_deck(row, column)
                    if deck.is_alive:
                        print("□", end=" ")
                    else:
                        if self.field[(row, column)].is_drowned:
                            print("x", end=" ")
                        else:
                            print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
