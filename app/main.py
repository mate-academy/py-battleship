class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self._create_decks()

    def _create_decks(self) -> None:
        start_row, start_column = self.start
        end_row, end_column = self.end
        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(start_row, column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, start_column))
        else:
            raise ValueError("Invalid ship position.")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def _is_sunk(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return False
        return True

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            if self._is_sunk():
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self._ships = []
        self._create_field(ships)
        self._validate_field()

    def _validate_field(self) -> None:
        single_deck = 0
        double_deck = 0
        three_deck = 0
        four_deck = 0

        for ship in self._ships:
            length = len(ship.decks)
            if length == 1:
                single_deck += 1
            elif length == 2:
                double_deck += 1
            elif length == 3:
                three_deck += 1
            elif length == 4:
                four_deck += 1
            else:
                raise ValueError("Invalid ship length.")

        if (
                len(self._ships) != 10
                or single_deck != 4
                or double_deck != 3
                or three_deck != 2
                or four_deck != 1
        ):
            raise ValueError("Invalid ship configuration.")

        for ship1 in self._ships:
            for ship2 in self._ships:
                if ship1 is not ship2:
                    if self._is_adjacent(ship1, ship2):
                        raise ValueError(
                            "Ships should not be located in neighboring cells."
                        )

    def _is_adjacent(self, first_ship: Ship, second_ship: Ship) -> bool:
        for first_ship_deck in first_ship.decks:
            for second_ship_deck in second_ship.decks:
                if self._are_cells_adjacent(first_ship_deck, second_ship_deck):
                    return True
        return False

    @staticmethod
    def _are_cells_adjacent(first_cell: Deck, second_cell: Deck) -> bool:
        dx = abs(first_cell.row - second_cell.row)
        dy = abs(first_cell.column - second_cell.column)
        return dx <= 1 and dy <= 1 and not (dx == 1 and dy == 1)

    def _create_field(self, ships: list) -> None:
        for ship in ships:
            start = min(ship[0], ship[1])
            end = max(ship[0], ship[1])
            new_ship = Ship(start, end)
            self._ships.append(new_ship)
            for row in range(start[0], end[0] + 1):
                for column in range(start[1], end[1] + 1):
                    self.field[(row, column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        symbols = {
            "empty": "~",
            "alive": u"\u25A1",
            "hit": "*",
            "drowned": "x"
        }
        for row in range(10):
            for column in range(10):
                cell = (row, column)
                if cell in self.field:
                    ship = self.field[cell]
                    deck = ship.get_deck(row, column)
                    if not ship.is_drowned:
                        if deck.is_alive:
                            print(symbols["alive"], end=" ")
                        else:
                            print(symbols["hit"], end=" ")
                    else:
                        print(symbols["drowned"], end=" ")
                else:
                    print(symbols["empty"], end=" ")
            print()
