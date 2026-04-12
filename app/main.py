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
        self.ships_list = [Ship(start, end) for start, end in ships]
        self.field = {}
        # Викликаємо валідацію ПЕРЕД фінальним заповненням словника field
        self._validate_field()
        # Заповнюємо робоче поле лише для перевіреного флоту
        for ship in self.ships_list:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        # Перевірка загальної кількості кораблів
        if len(self.ships_list) != 10:
            raise ValueError("Total number of ships must be 10!")

        # Перевірка складу флоту
        lengths = [len(ship.decks) for ship in self.ships_list]
        composition = {1: 4, 2: 3, 3: 2, 4: 1}
        for size, count in composition.items():
            if lengths.count(size) != count:
                raise ValueError(f"Invalid count for {size}-deck ships!")

        # Перевірка меж (0..9) та накладання (overlap)
        seen_coords = set()
        temp_map = {}
        for ship in self.ships_list:
            for deck in ship.decks:
                # Перевірка меж (Checklist #37)
                if not (0 <= deck.row <= 9 and 0 <= deck.column <= 9):
                    raise ValueError("Deck is out of field bounds!")

                # Перевірка накладання (Checklist #38)
                coords = (deck.row, deck.column)
                if coords in seen_coords:
                    raise ValueError("Ships overlap at the same coordinate!")

                seen_coords.add(coords)
                temp_map[coords] = ship

        # Перевірка сусідства (включаючи діагоналі)
        for row_idx, col_idx in seen_coords:
            current_ship = temp_map[(row_idx, col_idx)]
            for neighbor_row in range(row_idx - 1, row_idx + 2):
                for neighbor_col in range(col_idx - 1, col_idx + 2):
                    neighbor_pos = (neighbor_row, neighbor_col)

                    if (0 <= neighbor_row <= 9
                            and 0 <= neighbor_col <= 9
                            and neighbor_pos in temp_map):
                        if temp_map[neighbor_pos] != current_ship:
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
