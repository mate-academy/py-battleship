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

    def __eq__(self, other: Deck) -> bool:
        return self.row == other.row and self.column == other.column


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        self.decks = []
        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False

        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for ship_start, ship_end in ships:
            start_row, start_column = ship_start
            end_row, end_column = ship_end

            ship = Ship(ship_start, ship_end)

            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    self.field[(row, column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship:
            ship.fire(location[0], location[1])
            return "Hit!" if not ship.is_drowned else "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field.get((row, column))
                if ship:
                    if ship.is_drowned:
                        print("x", end="\t")
                    else:
                        if ship.get_deck(row, column).is_alive:
                            print("□", end="\t")
                        else:
                            print("*", end="\t")
                else:
                    print("~", end="\t")
            print("")

    def _validate_field(self) -> None:
        deck_counts = {ship: 0 for ship in self.field.values()}
        ship_counts = {i: 0 for i in range(1, 5)}

        if len(deck_counts) != 10:
            raise ValueError("The total number of the ships should be 10")

        for coord, ship in self.field.items():
            deck_counts[ship] += 1

        for deck in deck_counts.values():
            try:
                ship_counts[deck] += 1
            except KeyError:
                raise ValueError("There should be only 1-4 decks in the ships")

        for count in ship_counts:
            if ship_counts[count] + count != 5:
                raise ValueError(
                    f"There should be {5-count} "
                    f"{count}-deck ships"
                )

        ship_neighbors = {ship: None for ship in self.field.values()}
        for ship in ship_neighbors:

            neighbors = []
            for deck in ship.decks:
                for neighbor_list in ship_neighbors.values():
                    if neighbor_list is None:
                        break
                    if any(deck == neighbor for neighbor in neighbor_list):
                        raise ValueError(
                            "Ships shouldn't be located "
                            "in the neighboring cell in "
                            f"({deck.row}, {deck.column})"
                        )

                neighbors.append(Deck(deck.row, deck.column - 1))
                neighbors.append(Deck(deck.row, deck.column + 1))
                neighbors.append(Deck(deck.row - 1, deck.column))
                neighbors.append(Deck(deck.row + 1, deck.column))

                for neighbor in neighbors:
                    if neighbor in ship.decks:
                        neighbors.remove(neighbor)

            ship_neighbors[ship] = neighbors
