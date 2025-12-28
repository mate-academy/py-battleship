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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int]]]) -> None:
        self.size = 10
        self.ship_cells = [
            ["~" for _ in range(self.size)] for _ in range(self.size)
        ]
        if all(
                isinstance(cords, tuple) and len(cords) == 2
                for ship in ships for cords in ship
        ):
            self.ships = [
                Ship(start, end) for start, end in ships
            ]
        self.field = {}
        self._place_ships()
        self._validate_field()

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) not in self.field:
            return "Miss!"
        ship = self.field[(row, column)]
        if ship.fire(row, column):
            if ship.is_drowned:
                for deck in ship.decks:
                    self.ship_cells[deck.row][deck.column] = "x"
                return "Sunk!"
            self.ship_cells[row][column] = "*"
            return "Hit!"
        return "Miss!"

    def _place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.ship_cells[deck.row][deck.column] = u"\u25A1"
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Total number of ships must be 10")
        ship_lengths = [len(ship.decks) for ship in self.ships]
        if (
                (ship_lengths.count(1) != 4 or ship_lengths.count(2) != 3)
                or (ship_lengths.count(3) != 2)
                or (ship_lengths.count(4) != 1)
        ):
            raise ValueError("Invalid number of ships of each type")
        if not self._check_no_adjacent_ships():
            raise ValueError("Ships must not be adjacent")

    def _check_no_adjacent_ships(self) -> bool:
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        for (x_coord, y_coord) in self.field:
            for dx, dy in directions:
                nx, ny = x_coord + dx, y_coord + dy
                if ((0 <= nx < self.size and 0 <= ny < self.size)
                        and (nx, ny) in self.field and self.field[
                            (nx, ny)] != self.field[(x_coord, y_coord)]):
                    return False
        return True

    def print_field(self) -> None:
        for row in self.ship_cells:
            print(" ".join(row))
