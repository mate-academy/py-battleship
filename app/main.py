from typing import Dict, List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column})"


class Ship:
    def __init__(self, start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks: List[Deck] = []

        start_row, start_col = start
        end_row, end_col = end

        for row in range(start_row, end_row + 1):
            for column in range(start_col, end_col + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def shoot(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        deck.is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"

        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(
        self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships_list: List[Ship] = []

        for ship_coordinates in ships:
            start, end = ship_coordinates
            ship_object = Ship(start, end)
            self.ships_list.append(ship_object)

            for deck in ship_object.decks:
                self.field[(deck.row, deck.column)] = ship_object
        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships_list) != 10:
            raise ValueError("Должно быть ровно 10 кораблей!")

        sizes = [len(ship.decks) for ship in self.ships_list]
        expected_sizes = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        if sorted(sizes) != expected_sizes:
            raise ValueError("Неверный состав "
                             "кораблей (должно быть: 4x1, 3x2, 2x3, 1x4)!")

        for i, ship1 in enumerate(self.ships_list):
            for ship2 in self.ships_list[i + 1:]:
                for d1 in ship1.decks:
                    for d2 in ship2.decks:
                        if (abs(d1.row - d2.row) <= 1
                                and abs(d1.column - d2.column) <= 1):
                            raise ValueError("Корабли не "
                                             "должны касаться друг друга!")

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            row, column = location
            return ship.shoot(row, column)
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_cells = []
            for col in range(10):
                coord = (row, col)
                if coord in self.field:
                    ship = self.field[coord]
                    deck = ship.get_deck(row, col)

                    if ship.is_drowned:
                        row_cells.append("x")
                    elif not deck.is_alive:
                        row_cells.append("*")
                    else:
                        row_cells.append("□")
                else:
                    row_cells.append("~")
            print(" ".join(row_cells))
