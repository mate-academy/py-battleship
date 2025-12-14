class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True

    def hit(self) -> None:
        self.is_alive = False

    def __str__(self) -> str:
        return "*" if not self.is_alive else u"\u25A1"


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.decks = self._create_decks(start, end)
        self.is_drowned = False

    @staticmethod
    def _create_decks(start: tuple[int, int],
                      end: tuple[int, int]) -> list[Deck]:
        decks = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))
        return decks

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.hit()
                self.is_drowned = all(not d.is_alive for d in self.decks)
                return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = self._create_field()
        self._validate_field()

    def _create_field(self) -> list[list[str]]:
        field = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                field[deck.row][deck.column] = u"\u25A1"
        return field

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Incorrect number of ships.")

    def fire(self, location: tuple[int, int]) -> str:
        row, col = location
        for ship in self.ships:
            result = ship.fire(row, col)
            if result != "Miss!":
                self.field[row][col] = "x" if result == "Sunk!" else "*"
                return result
        return "Miss!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
