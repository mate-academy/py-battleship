class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = []

        if start[0] == end[0]:
            row = start[0]
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
        else:
            column = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        processed_ships = []
        for ship in ships:
            if isinstance(ship, Ship):
                processed_ships.append(ship)
            else:
                processed_ships.append(Ship(ship[0], ship[1]))

        self.ships = processed_ships
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ship_positions = {}

        self.place_ships()
        self._validate_field()

    def place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "□"
                self.ship_positions[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        from collections import Counter

        sizes = [len(ship.decks) for ship in self.ships]
        count = Counter(sizes)
        if count[4] != 1 or count[3] != 2 or count[2] != 3 or count[1] != 4:
            raise ValueError("Wrong number of ships")

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        occupied = set()

        for ship in self.ships:
            current_positions = {(d.row, d.column) for d in ship.decks}

            for deck in ship.decks:
                for row_offset, col_offset in directions:
                    check_row = deck.row + row_offset
                    check_col = deck.column + col_offset
                    if (check_row, check_col) in occupied:
                        raise ValueError("Ships touch each other")

            occupied.update(current_positions)

    def fire(self, location: tuple) -> str:
        row, column = location

        if (row, column) not in self.ship_positions:
            return "Miss!"

        ship = self.ship_positions[(row, column)]
        result = ship.fire(row, column)

        if result == "Hit!":
            self.field[row][column] = "*"
        elif result == "Sunk!":
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "x"

        return result

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
