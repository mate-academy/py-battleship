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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if [deck.row, deck.column] == [row, column]:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if True not in [deck.is_alive for deck in self.decks]:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int]]]) -> None:
        self.field = {
            ship: Ship(ship[0], ship[1])
            for ship in ships
        }

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            if self.field[ship].get_deck(location[0], location[1]):
                self.field[ship].fire(location[0], location[1])
                if self.field[ship].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for ship in self.field.values():
            for deck in ship.decks:
                if not deck.is_alive:
                    symbol = "x" if ship.is_drowned else "*"
                else:
                    symbol = u"\u25A1"
                field[deck.row][deck.column] = symbol
        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        single_deck = double_deck = three_deck = four_deck = 0
        for ship in self.field.values():
            length = len(ship.decks)
            if length == 1:
                single_deck += 1
            elif length == 2:
                double_deck += 1
            elif length == 3:
                three_deck += 1
            elif length == 4:
                four_deck += 1

        if not (single_deck == 4
                and double_deck == 3
                and three_deck == 2
                and four_deck == 1):
            raise ValueError("Incorrect number of ships")

        if len(self.field) != 10:
            raise ValueError("Total number of ships should be 10")

        def is_neighboring_cells(row: int, column: int) -> bool:
            for _row in range(max(0, row - 1), min(10, row + 2)):
                for _column in range(max(0, column - 1), min(10, column + 2)):
                    if _row == row and _column == column:
                        continue
                    if any(deck.row == _row and deck.column == _column
                           for ship in self.field.values()
                           for deck in ship.decks):
                        return True
            return False

        for ship in self.field.values():
            for deck in ship.decks:
                if is_neighboring_cells(deck.row, deck.column):
                    raise ValueError("Ships shouldn't be located "
                                     "in neighboring cells")
