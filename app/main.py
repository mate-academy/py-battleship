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
        self.is_drowned = is_drowned

        self.decks = []
        self.decks_cells = set()
        self.set_decks()

        self.decks_with_margin_cells = set()
        self.set_decks_with_margin_cells()

    def set_decks(self) -> None:
        if self.start[0] != self.end[0]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))
                self.decks_cells.add((i, self.start[1]))

        if self.start[1] != self.end[1]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
                self.decks_cells.add((self.start[0], i))

        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
            self.decks_cells.add((self.start[0], self.start[1]))

    def set_decks_with_margin_cells(self) -> None:
        for deck in self.decks:
            if deck.row == 0 and deck.column == 0:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column + 1),
                ])
            elif deck.row == 0 and deck.column == 9:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                    (deck.row + 1, deck.column),
                ])
            elif deck.row == 9 and deck.column == 0:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                ])
            elif deck.row == 9 and deck.column == 9:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                ])
            elif (
                    deck.row == 0
                    and deck.column != 0
                    and deck.column != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column + 1),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                ])
            elif (
                    deck.row == 9
                    and deck.column != 0
                    and deck.column != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column - 1),
                    (deck.row - 1, deck.column - 1),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                ])
            elif (
                    deck.column == 0
                    and deck.row != 0
                    and deck.row != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column + 1),
                    (deck.row + 1, deck.column),
                ])
            elif (
                    deck.column == 9
                    and deck.row != 0
                    and deck.row != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                    (deck.row + 1, deck.column),
                ])
            else:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                    (deck.row - 1, deck.column - 1),
                ])

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships: list[Ship] = []
        self.field = {}

        for ship in ships:
            ship_instance = Ship(ship[0], ship[1])
            self.ships.append(ship_instance)
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(location[0], location[1])

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise Exception("Number of ships must be 10")
        if sum(len(ship.decks) for ship in self.ships) != 20:
            raise Exception("There must be 4 single-deck ships, "
                            "3 double-deck ships, 2 three-deck ships "
                            "and 1 four-deck ship")
        for i in range(len(self.ships)):
            ship = self.ships[i]

            for count in range(i + 1, len(self.ships)):

                if len(ship.decks_with_margin_cells.intersection(
                    self.ships[count].decks_cells
                )) != 0:
                    raise Exception("Ships shouldn't be located "
                                    "in the neighboring cells "
                                    "(even if cells are neighbors "
                                    "by diagonal)")

    def print_field(self) -> None:
        field_matrix = []

        for _ in range(10):
            row_items = ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
            field_matrix.append(row_items)

        for location in self.field:
            ship = self.field.get(location)

            if ship.is_drowned:
                field_matrix[location[0]][location[1]] = "X"

            else:
                deck = ship.get_deck(location[0], location[1])

                if deck.is_alive:
                    field_matrix[location[0]][location[1]] = u"\u25A1"
                else:
                    field_matrix[location[0]][location[1]] = "*"

        print("\n".join(["".join(["{:4}".format(item) for item in row])
                         for row in field_matrix]))
