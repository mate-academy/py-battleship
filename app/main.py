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
        self.decks = []
        (row1, column1), (row2, column2) = start, end
        if row1 == row2:
            for column in range(
                    min(column1, column2), max(column1, column2) + 1
            ):
                self.decks.append(Deck(row1, column))
        elif column1 == column2:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, column1))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int]]]) -> None:
        self.field = {}
        for ship in ships:
            current_ship = Ship(*ship)
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["^" for _ in range(10)] for _ in range(10)]

        for deck_coordinates in self.field:
            ship = self.field[deck_coordinates]
            deck = ship.get_deck(*deck_coordinates)
            if deck.is_alive:
                field[deck.row][deck.column] = u"\u25A1"
            elif ship.is_drowned:
                field[deck.row][deck.column] = "x"
            else:
                field[deck.row][deck.column] = "*"

        for row in range(10):
            print(field[row])

    def _validate_field(self) -> None:
        ship_sizes = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in set(self.field.values()):
            ship_size = len(ship.decks)
            if ship_size in ship_sizes:
                ship_sizes[ship_size] += 1

        for ship_size, count in ship_sizes.items():
            if 5 - ship_size != count:
                raise ValueError("Invalid number of ships.")

        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        for (row, column), ship in self.field.items():
            for row_direction, column_direction in directions:
                neighbor_cell = (
                    row + row_direction, column + column_direction
                )
                if (
                    neighbor_cell in self.field
                    and self.field[neighbor_cell] != ship
                ):
                    raise ValueError("Ships are too close.")
