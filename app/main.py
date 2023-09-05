from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __sub__(self, other: Deck) -> list:
        if other.row > self.row:
            return [
                Deck(row, self.column)
                for row in range(self.row, other.row + 1)
            ]
        if other.column > self.column:
            return [
                Deck(self.row, column)
                for column in range(self.column, other.column + 1)
            ]
        return [Deck(self.row, self.column)]


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = Deck(*start) - Deck(*end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = not deck.is_alive
        if all(not ship_part.is_alive for ship_part in self.decks):
            self.is_drowned = not self.is_drowned


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship in ships:
            created_ship = Ship(*ship)
            for deck in created_ship.decks:
                self.field.update(
                    {(deck.row, deck.column): created_ship}
                )

    def fire(self, location: tuple) -> str:
        if (
                location in self.field
                and self.field.get(location).get_deck(*location).is_alive
        ):
            part_of_ship = self.field.get(location)
            part_of_ship.fire(*location)
            if not part_of_ship.is_drowned:
                return "Hit!"
            return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        non_empty_cells = sorted(self.field.keys())
        ship = self.field.get
        for row in range(0, 10):
            for column in range(0, 10):
                if not (row, column) in non_empty_cells:
                    print("~", end="")
                else:
                    if ship((row, column)).is_drowned:
                        print("x", end="")
                    elif ship((row, column)).get_deck(row, column).is_alive:
                        print(u"\u25A1", end="")
                    else:
                        print("*", end="")
                print("\t", end="")
            print("\n", end="")
