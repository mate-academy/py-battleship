from collections import Counter


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        start_row, start_col = start[0], start[1]
        end_row, end_col = end[0], end[1]
        if start_row != end_row and start_col != end_col:
            raise ValueError("Ship can only be vertical or horizontal.")
        len_cols = max(start_col, end_col) - min(start_col, end_col)
        len_rows = max(start_row, end_row) - min(start_row, end_row)
        if len_cols > 3 or len_rows > 3:
            raise ValueError("Ship can not be longer than 4")
        if start_row == end_row and start_col == end_col:
            self.decks.append(Deck(start_row, end_col))
        elif start_row == end_row:
            left = min(start_col, end_col)
            right = max(start_col, end_col)
            for i in range(left, right + 1):
                self.decks.append(Deck(start_row, i))
        elif start_col == end_col:
            up = min(start_row, end_row)
            down = max(start_row, end_row)
            for i in range(up, down + 1):
                self.decks.append(Deck(i, start_col))

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        result = self.get_deck(row, column)

        if not result.is_alive:
            raise ValueError("You already fired at this location.")

        result.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship in ships:
            start, end = ship[0], ship[1]
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(*location)

        return "Miss!"

    def print_field(self) -> None:
        matrix = 10
        symbols = {
            "water": "░",
            "alive": "█",
            "hit": "✖",
            "sunk": "☠",
        }
        for row in range(matrix):
            for col in range(matrix):
                cords = (row, col)
                if cords in self.field:
                    ship = self.field[cords]
                    deck = ship.get_deck(*cords)
                    if ship.is_drowned:
                        print(symbols["sunk"], end="  ")
                    elif not deck.is_alive:
                        print(symbols["hit"], end="  ")
                    else:
                        print(symbols["alive"], end="  ")
                else:
                    print(symbols["water"], end="  ")
            print()

    def _validate_field(self) -> None:
        ship_sizes = (
            Counter(len(ship.decks) for ship in set(self.field.values()))
        )
        if ship_sizes[4] != 1:
            raise ValueError("Could be only one 4-deck ship")
        elif ship_sizes[3] != 2:
            raise ValueError("Could be only two 3-deck ship")
        elif ship_sizes[2] != 3:
            raise ValueError("Could be only three 2-deck ship")
        elif ship_sizes[1] != 4:
            raise ValueError("Could be only four 1-deck ship")
        elif sum(ship_sizes.values()) != 10:
            raise ValueError("Available only 10 ships")

        occupied = set(self.field.keys())
        for row, col in occupied:
            for r_cl in range(row - 1, row + 2):
                for c_cl in range(col - 1, col + 2):
                    if (r_cl, c_cl) in occupied and (r_cl, c_cl) != (row, col):
                        current_ship = self.field[(row, col)]
                        neighbour_ship = self.field[(r_cl, c_cl)]

                        if current_ship is not neighbour_ship:
                            raise ValueError(
                                "Ships shouldn't "
                                "be located in neighboring cells"
                            )
