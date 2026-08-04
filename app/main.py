class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.start = start
        self.end = end
        self.decks = []
        self._generate_decks(start, end)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck:
            target_deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)

    def _generate_decks(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[Deck]:
        row_start, col_start = start
        row_end, col_end = end

        if row_start == row_end:
            for col in range(
                    min(col_start, col_end), max(col_start, col_end) + 1
            ):
                self.decks.append(Deck(row_start, col))
        else:
            for row in range(
                    min(row_start, row_end), max(row_start, row_end) + 1
            ):
                self.decks.append(Deck(row, col_start))
        return self.decks


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship_coords in ships:
            ship = Ship(ship_coords[0], ship_coords[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if ship.is_drowned:
                        row_str += "x\t"
                    elif not deck.is_alive:
                        row_str += "*\t"
                    else:
                        row_str += u"\u25A1\t"
                else:
                    row_str += "~\t"
            print(row_str.strip())

    def _validate_field(self) -> ValueError | None:
        unique_ships = set(self.field.values())
        if len(unique_ships) != 10:
            raise ValueError("The total number of the ships should be 10")

        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in unique_ships:
            deck_count = len(ship.decks)
            if deck_count in ship_counts:
                ship_counts[deck_count] += 1
            else:
                raise ValueError(f"Invalid ship length: {deck_count}")

        if (ship_counts[1] != 4 or ship_counts[2] != 3
                or ship_counts[3] != 2 or ship_counts[4] != 1):
            raise ValueError("Invalid fleet composition")

        for (row, col), ship in self.field.items():
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    if d_row == 0 and d_col == 0:
                        continue
                    neighbor = (row + d_row, col + d_col)
                    if neighbor in self.field and self.field[neighbor] != ship:
                        raise ValueError(
                            "Ships shouldn't be located "
                            "in the neighboring cells"
                        )
