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
        self.is_drowned = is_drowned
        self.decks = []
        x1, y1 = start
        x2, y2 = end
        for x_coord in range(x1, x2 + 1):
            for y_coord in range(y1, y2 + 1):
                self.decks.append(Deck(x_coord, y_coord))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        current_deck = self.get_deck(row, column)
        current_deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive is True:
                self.is_drowned = False
                return
            else:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        matrix = [["~" for _ in range(10)] for _ in range(10)]

        ships = set(self.field.values())
        for ship in ships:
            if ship.is_drowned:
                for deck in ship.decks:
                    matrix[deck.row][deck.column] = "x"
            else:
                for deck in ship.decks:
                    if deck.is_alive:
                        matrix[deck.row][deck.column] = u"\u25A1"
                    else:
                        matrix[deck.row][deck.column] = "*"

        for row in matrix:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(set(self.field.values())) != 10:
            raise ValueError(f"Should be 10 ships "
                             f"instead of {len(self.field)}")

        ships = sorted([len(ship.decks) for ship in set(self.field.values())])
        if ships != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Should be 4 single-deck ships, "
                             "3 double-deck ships, "
                             "2 three-deck ships, "
                             "1 four-deck ship")

        neighbors = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]

        occupied_cells = set()
        for ship in set(self.field.values()):
            for deck in ship.decks:
                occupied_cells.add((deck.row, deck.column))
                row, col = deck.row, deck.column

                for drow, dcol in neighbors:
                    neighbor = (row + drow, col + dcol)
                    decks = [(deck.row, deck.column) for deck in ship.decks]
                    if neighbor in occupied_cells and neighbor not in decks:
                        raise ValueError(f"Ships are too close! "
                                         f"Error at {neighbor}")
                occupied_cells.add((row, col))
