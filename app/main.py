class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:
        start_x, start_y = self.start
        end_x, end_y = self.end

        decks = []

        if start_x == end_x:
            ship_len = abs(end_y - start_y) + 1
            for i in range(ship_len):
                decks.append(Deck(start_x, min(start_y, end_y) + i))
        elif start_y == end_y:
            ship_len = abs(end_x - start_x) + 1
            for i in range(ship_len):
                decks.append(Deck(min(start_x, end_x) + i, start_y))
        else:
            raise ValueError(
                "The ship should have only horizontal or only vertical cells"
            )

        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if not deck:
            return "Miss!"
        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"

    def __str__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {
            (deck.row, deck.column):
                ship for ship in self.ships for deck in ship.decks
        }
        self._validate_field()

    def fire(self, location: tuple) -> tuple | str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(*location)
            return result
        return "Miss!"

    def print_field(self) -> None:
        grid = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive and not ship.is_drowned:
                    grid[deck.row][deck.column] = "□"
                elif not deck.is_alive and not ship.is_drowned:
                    grid[deck.row][deck.column] = "*"
                elif ship.is_drowned:
                    grid[deck.row][deck.column] = "x"
        for i in range(10):
            print(" ".join(grid[i]))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The number of ships should be 10!")

        lengths = [len(ship.decks) for ship in self.ships]
        if (
            (lengths.count(4) != 1)
            or (lengths.count(3) != 2)
            or (lengths.count(2) != 3 or lengths.count(1) != 4)
        ):
            raise ValueError("The wrong number of ships!")

        occupied = set()
        for ship in self.ships:
            for deck in ship.decks:
                x_coord = deck.row
                y_coord = deck.column
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (x_coord + dx, y_coord + dy) in occupied:
                            raise ValueError("The ships can't be so close!")
            coords = [(deck.row, deck.column) for deck in ship.decks]
            occupied.update(coords)
