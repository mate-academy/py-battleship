class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.decks = self._create_decks(start, end)
        self.is_drowned = False

    def _create_decks(self, start: tuple[int, int],
                      end: tuple[int, int]) -> list[Deck]:
        decks = []
        start_row, start_col = start
        end_row, end_col = end

        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                decks.append(Deck(start_row, col))
        elif start_col == end_col:
            for row in range(start_row, end_row + 1):
                decks.append(Deck(row, start_col))
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


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]
                 ) -> None:
        self.size = 10
        self.field = [["~" for _ in range(self.size)]
                      for _ in range(self.size)]
        self.ships = [Ship(*ship) for ship in ships]
        self._place_ships()

    def _get_ship_cells(self, start: tuple[int, int],
                        end: tuple[int, int]
                        ) -> list[tuple[int, int]]:
        cells = []
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                cells.append((start_row, col))
        elif start_col == end_col:
            for row in range(start_row, end_row + 1):
                cells.append((row, start_col))
        return cells

    def _place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = u"\u25A1"

    def fire(self, location: tuple[int, int]) -> str:
        row, col = location
        if self.field[row][col] == "~":
            return "Miss!"
        for ship in self.ships:
            if ship.fire(row, col):
                self.field[row][col] = "*"
                if ship.is_drowned:
                    for deck in ship.decks:
                        self.field[deck.row][deck.column] = "x"
                    return "Sunk!"
                return "Hit!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
