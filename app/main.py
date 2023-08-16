class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        for i in range(start[0], end[0] + 1):
            for j_ in range(start[1], end[1] + 1):
                self.decks.append(Deck(i, j_))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return False
        self.is_drowned = True
        return True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for start_ship, end_ship in ships:
            ship = Ship(start_ship, end_ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) in self.field:
            ship = self.field[(row, column)]
            deck = ship.get_deck(row, column)
            if deck.is_alive:
                ship.fire(row, column)
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for i in range(1, 11):
            for j_ in range(1, 11):
                cell = self.field.get((i, j_))
                if cell is None:
                    print("~", end=" ")
                elif cell.is_drowned:
                    print("x", end=" ")
                elif (deck.is_alive for deck in cell.decks):
                    print("*", end=" ")
                else:
                    print(u"\u25A1", end=" ")

    def _validate_field(self) -> None:
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            length = max(ship[1][0] - ship[0][0], ship[1][1] - ship[0][1]) + 1
            ship_counts[length] += 1

            for i in range(ship[0][0] - 1, ship[1][0] + 2):
                for j_ in range(ship[0][1] - 1, ship[1][1] + 2):
                    if (i, j_) in self.field:
                        raise ValueError("Ships should not be located "
                                         "in neighboring cells.")

        if ship_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Incorrect number of ships of each length.")
