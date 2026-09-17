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


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] != end[0]:
            for i in range(
                min(start[0], end[0]),
                max(start[0], end[0]) + 1
            ):
                self.decks.append(Deck(i, end[1]))
        else:
            for i in range(
                min(start[1], end[1]),
                max(start[1], end[1]) + 1
            ):
                self.decks.append(Deck(start[0], i))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        damaged_deck = self.get_deck(row, column)
        if damaged_deck:
            damaged_deck.is_alive = False
            if not any(status.is_alive for status in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}
        for ship in ships:
            new_ship = Ship(*ship)
            self.ships.append(new_ship)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for column in range(10):
                ship = self.field.get((row, column))
                if ship is None:
                    line += "~"
                else:
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        line += "x"
                    elif deck.is_alive:
                        line += "\u25A1"
                    else:
                        line += "*"
            print(line)

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be 10 ships")
        sizes = sorted(len(ship.decks) for ship in self.ships)
        if sizes != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Invalid ships configuration")
        for ship in self.ships:
            for deck in ship.decks:
                row, column = deck.row, deck.column
                for neighbor_row in range(row - 1, row + 2):
                    for neighbor_column in range(column - 1, column + 2):
                        if (neighbor_row, neighbor_column) == (row, column):
                            continue
                        if (neighbor_row, neighbor_column) in self.field:
                            other_ship = self.field[
                                (neighbor_row, neighbor_column)
                            ]
                            if other_ship is not ship:
                                raise ValueError(
                                    "Ships can't be located "
                                    "next to each other"
                                )
