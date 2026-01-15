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
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks: dict[tuple[int, int], Deck] = {}
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks[(row, column)] = Deck(row, column)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        return self.decks.get((row, column))

    def fire(self, row: int, column: int) -> str:
        if (row, column) in self.decks:
            self.decks[(row, column)].is_alive = False

            if not any(deck.is_alive for deck in self.decks.values()):
                self.is_drowned = True
                return "Sunk!"

            return "Hit!"

        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        for start, end in ships:
            ship = Ship(start, end)
            for row in range(start[0], end[0] + 1):
                for column in range(start[1], end[1] + 1):
                    self.field[(row, column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)

        return "Miss!"

    def _validate_field(self) -> None:
        assert len(self.field) == 20, "total occupied cells must be 20"

        ships = set(self.field.values())
        assert len(ships) == 10, "must be exactly 10 ships on the field"

        counter = {i: 0 for i in range(1, 5)}
        reserved = set()
        for ship in ships:
            start, end = ship.start, ship.end
            assert start[0] == end[0] or start[1] == end[1], "wrong shape"

            num_decks = len(ship.decks)
            assert num_decks in counter, \
                f"ship with {num_decks} decks not allowed"
            counter[num_decks] += 1

            for location in ship.decks.keys():
                assert location not in reserved, "ship is too close to another"

            for row in range(start[0] - 1, end[0] + 2):
                for column in range(start[1] - 1, end[1] + 2):
                    reserved.add((row, column))

        for num_decks, amount in counter.items():
            assert amount == 5 - num_decks, \
                (f"There is {amount} ships of length {num_decks} "
                 f"(must be exactly {5 - num_decks} ships)")

    def print_field(self) -> None:
        rows = []
        for row in range(10):
            row_values = []
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    if ship.is_drowned:
                        row_values.append("x")
                    elif ship.decks[location].is_alive:
                        row_values.append("□")
                    else:
                        row_values.append("*")
                else:
                    row_values.append("~")
            rows.append(" ".join(row_values))

        print("\n".join(rows))
