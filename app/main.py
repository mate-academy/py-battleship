from typing import Tuple, Optional


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
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        r1, c1 = start
        r2, c2 = end

        if r1 != r2 and c1 != c2:
            raise ValueError("Ships must be horizontal or vertical, "
                             "not diagonal or rectangular.")

        if r1 == r2:
            for c_var in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, c_var))
        else:
            for r_var in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(r_var, c1))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        if deck and deck.is_alive:
            deck.is_alive = False

            self.is_drowned = all(
                not d.is_alive for d in self.decks
            )


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10.")

        sizes_count = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            size = len(ship.decks)
            if size not in sizes_count:
                raise ValueError(f"Invalid ship size detected: {size}")

            sizes_count[size] += 1

            for deck in ship.decks:
                if not (0 <= deck.row < 10 and 0 <= deck.column < 10):
                    raise ValueError(f"Ship deck {(deck.row, deck.column)} "
                                     f"is out of bounds.")

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        neighbor = (deck.row + dr, deck.column + dc)
                        if (neighbor in self.field
                                and self.field[neighbor] != ship):
                            raise ValueError("Ships shouldn't be located "
                                             "in the neighboring cells.")

        expected_sizes = {1: 4, 2: 3, 3: 2, 4: 1}
        if sizes_count != expected_sizes:
            raise ValueError(f"Invalid distribution of ships. "
                             f"Expected {expected_sizes}, "
                             f"got {sizes_count}")

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        row, column = location
        ship = self.field[location]

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for r_coords in range(10):
            row_symbols = []
            for c_coords in range(10):
                if (r_coords, c_coords) in self.field:
                    ship = self.field[(r_coords, c_coords)]
                    deck = ship.get_deck(r_coords, c_coords)

                    if ship.is_drowned:
                        row_symbols.append("x")
                    elif not deck.is_alive:
                        row_symbols.append("*")
                    else:
                        row_symbols.append(u"\u25A1")  # □
                else:
                    row_symbols.append("~")

            print("  ".join(row_symbols))


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )
