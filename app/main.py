class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, alive={self.is_alive})"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> list[Deck]:
        (r1, c1), (r2, c2) = self.start, self.end
        decks = []
        if r1 == r2:  # horizontal ship
            for col in range(min(c1, c2), max(c1, c2) + 1):
                decks.append(Deck(r1, col))
        elif c1 == c2:  # vertical ship
            for row in range(min(r1, r2), max(r1, r2) + 1):
                decks.append(Deck(row, c1))
        else:
            raise ValueError("Ships must be horizontal or vertical")
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None or not deck.is_alive:
            return "Miss!"
        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(*location)

    def print_field(self) -> None:
        board = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    board[deck.row][deck.column] = "□"
                elif ship.is_drowned:
                    board[deck.row][deck.column] = "x"
                else:
                    board[deck.row][deck.column] = "*"
        for row in board:
            print(" ".join(row))

    def _validate_field(self) -> None:
        from collections import Counter
        sizes = [len(ship.decks) for ship in self.ships]
        counter = Counter(sizes)
        if counter[1] != 4 or counter[2] != 3:
            if counter[3] != 2 or counter[4] != 1:
                raise ValueError("Incorrect fleet composition")
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships")
        occupied = set(self.field.keys())
        for rr, cc in occupied:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == dc == 0:
                        continue
                    nr, nc = rr + dr, cc + dc
                    if (nr, nc) in occupied and (nr, nc) not in self.field:
                        raise ValueError("Ships too close!")
