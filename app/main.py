class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        row1, column1 = start
        row2, column2 = end

        if row1 == row2:
            for col in range(min(column1, column2), max(column1, column2) + 1):
                self.decks.append(Deck(row1, col))
        elif column1 == column2:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, column1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [
            ship if isinstance(ship, Ship) else Ship(ship[0], ship[1])
            for ship in ships
        ]
        self._validate_field()
        self.field = {}
        self.misses = set()
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            row, column = location
            ship.fire(row, column)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"

        self.misses.add(location)
        return "Miss!"

    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)

    def print_field(self) -> None:
        for row in range(10):
            row_symbols = []
            for column in range(10):
                coord = (row, column)

                if coord in self.misses:
                    row_symbols.append("~")
                elif coord in self.field:
                    ship = self.field[coord]
                    deck = next(
                        d for d in ship.decks
                        if d.row == row
                        and d.column == column
                    )
                    if ship.is_drowned:
                        row_symbols.append("x")
                    elif deck.is_alive:
                        row_symbols.append(u"\u25A1")
                    else:
                        row_symbols.append("*")
                else:
                    row_symbols.append("~")
            print(" ".join(row_symbols))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of ships should be 10.")

        lengths = [len(ship.decks) for ship in self.ships]
        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}

        for length, expected_count in expected_counts.items():
            if lengths.count(length) != expected_count:
                raise ValueError(
                    f"There should be {expected_count} "
                    f"ships with length {length}."
                )

        all_decks = {}
        for ship in self.ships:
            for deck in ship.decks:
                coord = (deck.row, deck.column)
                if coord in all_decks:
                    raise ValueError("Ships cannot overlap.")
                all_decks[coord] = ship

        for current_ship in self.ships:
            for deck in current_ship.decks:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        neighbor = (deck.row + dr, deck.column + dc)
                        if (neighbor in all_decks
                                and all_decks[neighbor]
                                is not current_ship):
                            raise ValueError(
                                "Ships shouldn't be located "
                                "in neighboring cells."
                            )
