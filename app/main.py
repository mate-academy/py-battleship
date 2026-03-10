from __future__ import annotations


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
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        r1, c1 = start
        r2, c2 = end
        self.is_drowned = is_drowned
        self.decks = []

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        else:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        elif not deck.is_alive:
            return "Sunk!" if self.is_drowned else "Hit!"
        else:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def _validate_field(self) -> None:
        unique_ships = set(self.field.values())
        if len(unique_ships) != 10:
            raise ValueError("Total number of ships must be 10")
        sizes = [len(ship.decks) for ship in unique_ships]
        if sizes.count(1) != 4 or sizes.count(2) != 3:
            raise ValueError("Must have 4 single-deck and 3 double-deck ships")
        if sizes.count(3) != 2 or sizes.count(4) != 1:
            raise ValueError("Must have 2 three-deck and 1 four-deck ship")
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1),
        ]
        for (row, col), ship in self.field.items():
            for dr, dc in neighbors:
                neighbor = (row + dr, col + dc)
                if neighbor in self.field and self.field[neighbor] is not ship:
                    raise ValueError("Ships must not be in neighboring cells")

    def print_field(self) -> None:
        for row in range(10):
            line_parts = []
            for col in range(10):
                cell = (row, col)
                if cell not in self.field:
                    line_parts.append("~")
                else:
                    ship = self.field[cell]
                    deck = ship.get_deck(row, col)
                    assert deck is not None
                    if ship.is_drowned:
                        line_parts.append("x")
                    elif not deck.is_alive:
                        line_parts.append("*")
                    else:
                        line_parts.append("\u25A1")
            print("\t".join(line_parts))

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        row, column = location
        return ship.fire(row, column)
