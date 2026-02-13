from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def fire(self) -> bool:
        self.is_alive = False
        return self.is_alive

    def __repr__(self) -> str:
        return "□" if self.is_alive else "x"


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.create_decks(start, end)

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> List[Deck]:
        decks = []
        if start[0] == end[0]:  # Horizontal
            first_row = start[0]
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                decks.append(Deck(first_row, col))
        elif start[1] == end[1]:  # Vertical
            first_col = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                decks.append(Deck(row, first_col))
        return decks

    def fire(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.fire()
                if all(not deck.is_alive for deck in self.decks):
                    self.is_drowned = True
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        return "".join(str(deck) for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = [Ship(start, end) for start, end in ships]
        self.place_ships()
        self._validate_field()

    def place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                row, col = deck.row, deck.column
                self.field[row][col] = "□"

    def fire(self, location: tuple) -> str:
        row, col = location
        for ship in self.ships:
            result = ship.fire(row, col)

            if result == "Hit!":
                self.field[row][col] = "*"
                return result

            if result == "Sunk!":
                for deck in ship.decks:
                    self.field[deck.row][deck.column] = "x"
                return result

        return "Miss!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        ship_lengths = [len(ship.decks) for ship in self.ships]
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships.")
        if ship_lengths.count(1) != 4:
            raise ValueError("There should be exactly 4 single-deck ships.")
        if ship_lengths.count(2) != 3:
            raise ValueError("There should be exactly 3 double-deck ships.")
        if ship_lengths.count(3) != 2:
            raise ValueError("There should be exactly 2 three-deck ships.")
        if ship_lengths.count(4) != 1:
            raise ValueError("There should be exactly 1 four-deck ship.")
        if not self._check_no_neighbors():
            raise ValueError("Ships should not be located "
                             "in neighboring cells.")

    def _check_no_neighbors(self) -> bool:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)
                      ]
        for ship in self.ships:
            for deck in ship.decks:
                row, col = deck.row, deck.column
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if (0 <= nr < 10
                            and 0 <= nc < 10
                            and self.field[nr][nc] == "□"
                            and (nr, nc)
                            not in [(d.row, d.column) for d in ship.decks]):
                        return False
        return True
