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

        self.decks = []
        self.length = None
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

    @property
    def get_length(self) -> int:
        self.length = max(
            self.end[1] - self.start[1], self.end[0] - self.start[0]
        ) + 1
        return self.length

    @property
    def get_decks(self) -> list[Deck]:
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))
        return self.decks

    def get_deck(self, row: int, column: int) -> str:
        for deck in self.get_decks:
            if deck.row == row and deck.column == column:
                return self.fire(deck)

    def fire(self, deck: Deck) -> str:
        if self.is_drowned is False:
            deck.is_alive = False
            self.length -= 1
            if self.length == 0:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[tuple[int, int]]]]
    ) -> None:

        self.field = {}
        self.ships = ships
        self.field.update({coord: Ship(coord[0], coord[1]) for coord in ships})
        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise Exception("the total number of the ships should be 10")
        length_ships = [self.field[ship].get_length for ship in self.field]
        if length_ships.count(4) != 1:
            raise Exception("there should be 1 four-deck ship")
        if length_ships.count(3) != 2:
            raise Exception("there should be 2 three-deck ships")
        if length_ships.count(2) != 3:
            raise Exception("there should be 3 double-deck ships")
        if length_ships.count(1) != 4:
            raise Exception("there should be 4 single-deck ships")
        neighboring_cells = list(self.field.keys())
        for cell in neighboring_cells:
            for other_cell in neighboring_cells:
                if cell == other_cell:
                    continue
                if cell[0][0] == cell[1][0] \
                        and cell[0][0] == other_cell[0][0] == other_cell[1][0]:
                    if cell[0][1] == other_cell[0][1] \
                            or cell[0][1] == other_cell[0][1] + 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                    if cell[1][1] == other_cell[0][1] \
                            or cell[1][1] == other_cell[0][1] - 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                if cell[0][1] == cell[1][0] \
                        and cell[0][1] == other_cell[0][1] == other_cell[1][1]:
                    if cell[0][0] == other_cell[0][0] \
                            or cell[0][0] == other_cell[0][0] + 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                    if cell[0][0] == other_cell[0][0] \
                            or cell[0][0] == other_cell[0][0] - 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            cell_row, cell_column = location[0], location[1]

            if cell_row == ship[0][0] and cell_row == ship[1][0]:
                if ship[1][1] >= cell_column >= ship[0][1]:
                    return self.field[ship].get_deck(cell_row, cell_column)

            if cell_column == ship[0][1] and cell_column == ship[1][1]:
                if ship[1][0] >= cell_row >= ship[0][0]:
                    return self.field[ship].get_deck(cell_row, cell_column)
        return "Miss!"

    def print_field(self) -> None:
        battle_field = ["~"] * 10
        for row in range(len(battle_field)):
            for cell in self.field.values():
                if cell.start[0] == row:
                    for deck in cell.get_decks:
                        if deck.row == row:
                            if deck.is_alive:
                                battle_field[deck.column] = "\u25A1"
                            battle_field[deck.column] = "*"
            for cell in self.field.values():
                if cell.start[0] == row and cell.is_drowned:
                    for column in range(cell.start[1], cell.end[1] + 1):
                        battle_field[column] = "X"
            print(" ".join(battle_field))
            battle_field = ["~"] * 10
