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
    def __init__(self, start: int, end: int) -> None:
        self.decks = []
        row1, col1 = start
        row2, col2 = end

        if row1 == row2:
            for col in range(col1, col2 + 1):
                self.decks.append(Deck(row1, col))
        else:
            for row in range(row1, row2 + 1):
                self.decks.append(Deck(row, col1))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []

        for ship_coords in ships:
            ship = Ship(*ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        grid = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    grid[deck.row][deck.column] = "□"
                else:
                    if all(not d.is_alive for d in ship.decks):
                        grid[deck.row][deck.column] = "x"
                    else:
                        grid[deck.row][deck.column] = "*"

        for row in grid:
            print(" ".join(row))

    def _validate_field(self) -> bool:
        ship_sizes = [len(ship.decks) for ship in self.ships]

        if sorted(ship_sizes) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Invalid ship distribution.")

        def is_neighbor(cell1: list, cell2: list) -> bool:
            return (abs(cell1[0] - cell2[0]) <= 1
                    and abs(cell1[1] - cell2[1]) <= 1)

        occupied_cells = set(self.field.keys())
        for ship in self.ships:
            for deck in ship.decks:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        neighbor = (deck.row + dr, deck.column + dc)
                        if (neighbor in occupied_cells
                                and neighbor not in self.field):
                            raise ValueError("Ships should not be adjacent.")
