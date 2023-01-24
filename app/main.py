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

    def __repr__(self) -> str:
        return f"Deck({self.row} {self.column}), {self.is_alive}"


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False) -> None:

        self.is_drowned = is_drowned
        if start == end:
            self.decks = [Deck(start[0], end[1])]
        elif start[0] == end[0]:
            self.decks = [Deck(start[0], i)
                          for i in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            self.decks = [Deck(i, start[1])
                          for i in range(start[0], end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:

        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not list(filter(lambda deck: deck.is_alive, self.decks)):
            self.is_drowned = True

    def __repr__(self) -> str:
        if self.is_drowned:
            return "Drowned ship"
        return "Alive ship"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:

        self.ships = [Ship(*coordinates) for coordinates in ships]
        self._validate_field()
        self.field: dict = {}
        for ship in self.ships:
            ship_field = {(deck.row, deck.column): ship for deck in ship.decks}
            self.field.update(ship_field)

    def _validate_ships_count(self) -> None:

        assert len(self.ships) == 10

    def _validate_ship_sizes(self) -> None:

        ship_sizes = {}
        for ship in self.ships:
            ship_sizes[len(ship.decks)] = ship_sizes.get(
                len(ship.decks), 0
            ) + 1
        assert ship_sizes == {4: 1, 2: 3, 3: 2, 1: 4}

    def _validate_field(self) -> None:

        self._validate_ships_count()
        self._validate_ship_sizes()

    def fire(self, location: tuple[int, int]) -> str:

        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:

        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].get_deck(
                            row, column).is_alive:
                        print("O", end=" " * 3)
                    else:
                        print("X", end=" " * 3)
                else:
                    print("~", end=" " * 3)
            print()
