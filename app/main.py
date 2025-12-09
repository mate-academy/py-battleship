from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks(self.start, self.end)

    def _create_decks(self,
                      start: tuple[int, int],
                      end: tuple[int, int]) -> List[Deck]:
        (r1, c1), (r2, c2) = start, end
        decks = []
        if r1 == r2:
            for column in range(min(c1, c2), max(c1, c2) + 1):
                decks.append(Deck(r1, column))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                decks.append(Deck(row, c1))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def check_drowned(self) -> bool:
        if all(not decks.is_alive for decks in self.decks):
            self.is_drowned = True
        return self.is_drowned

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.ships = [Ship(*coords) for coords in ships]
        self.field = {}
        self._build_fields()
        self._validate_field()

    def _build_fields(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        length = [len(ship.decks) for ship in self.ships]
        if len(self.ships) != 10:
            raise ValueError("Must be exactly 10 ships")
        if (length.count(4) != 1
                or length.count(3) != 2
                or length.count(2) != 3
                or length.count(1) != 4):
            raise ValueError("Wrong number of ships by size")

        occupied = set(self.field.keys())
        for (row, column) in occupied:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    neighbour = (row + dr, column + dc)
                    if neighbour in occupied and neighbour != (row, column):
                        if self.field[neighbour] != self.field[(row, column)]:
                            raise ValueError("Ships are touching!")

    def print_field(self) -> None:
        for row in range(10):
            rows = []
            for column in range(10):
                if (row, column) not in self.field:
                    rows.append("~")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        rows.append(u"\u25A1")
                    elif not ship.is_drowned:
                        rows.append("*")
                    else:
                        rows.append("x")
            print("".join(rows))

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) not in self.field:
            return "Miss!"
        ship = self.field[(row, column)]
        ship.fire(row, column)
        if ship.check_drowned():
            return ("Sunk!")
        return ("Hit!")
