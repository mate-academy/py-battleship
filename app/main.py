from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        row_start, col_start = start
        row_end, col_end = end

        for row_idx in range(
            min(row_start, row_end), max(row_start, row_end) + 1
        ):
            for col_idx in range(
                min(col_start, col_end), max(col_start, col_end) + 1
            ):
                self.decks.append(Deck(row_idx, col_idx))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships_list = []

        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships_list.append(new_ship)
            for deck in new_ship.decks:
                # Перевірка на вихід за межі поля 10x10
                if not (0 <= deck.row < 10 and 0 <= deck.column < 10):
                    raise ValueError("Deck is out of field bounds!")
                # Перевірка на накладання кораблів
                if (deck.row, deck.column) in self.field:
                    raise ValueError("Ships overlap at the same coordinate!")
                self.field[(deck.row, deck.column)] = new_ship

        self._validate_field()

    def _validate_field(self) -> None:
        # Перевірка загальної кількості кораблів
        if len(self.ships_list) != 10:
            raise ValueError("Total number of ships must be 10!")

        # Перевірка складу флоту за кількістю палуб
        lengths = [len(ship.decks) for ship in self.ships_list]
        composition = {1: 4, 2: 3, 3: 2, 4: 1}
        for size, count in composition.items():
            if lengths.count(size) != count:
                raise ValueError(f"Invalid count for {size}-deck ships!")

        # Перевірка наявності сусідів (включаючи діагоналі)
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    current_ship = self.field[(row, col)]
                    # Перевірка 8 сусідніх клітинок
                    for neighbor_row in range(row - 1, row + 2):
                        for neighbor_col in range(col - 1, col + 2):
                            neighbor_pos = (neighbor_row, neighbor_col)
                            if (0 <= neighbor_row < 10
                                    and 0 <= neighbor_col < 10
                                    and neighbor_pos in self.field):
                                if self.field[neighbor_pos] != current_ship:
                                    raise ValueError("Neighboring ships!")

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        target_ship = self.field[location]
        target_ship.fire(location[0], location[1])

        if target_ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row_idx in range(10):
            row_display = []
            for col_idx in range(10):
                if (row_idx, col_idx) not in self.field:
                    row_display.append("~")
                else:
                    ship = self.field[(row_idx, col_idx)]
                    deck = ship.get_deck(row_idx, col_idx)
                    if ship.is_drowned:
                        row_display.append("x")
                    elif not deck.is_alive:
                        row_display.append("*")
                    else:
                        row_display.append("□")
            print(" ".join(row_display))
