class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.is_drowned = is_drowned
        self.decks = [Deck(i, j)
                      for i in range(start[0], end[0] + 1)
                      for j in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for desk in self.decks:
            if desk.row == row and desk.column == column:
                return desk

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(desk.is_alive for desk in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = dict()
        for unit in ships:
            ship = Ship(*unit)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        matrix = [["~" for _ in range(10)] for _ in range(10)]
        for cell in self.field:
            row, column = cell
            ship = self.field[cell]
            if ship.is_drowned:
                matrix[row][column] = "x"
            elif ship.get_deck(row, column).is_alive:
                matrix[row][column] = u"\u25A1"
            else:
                matrix[row][column] = "*"

        for item in matrix:
            print(*item)

    def _validate_field(self) -> None:
        ships = set(self.field.values())
        if len(ships) != 10:
            print("The total number of the ships should be 10")
        numbers_deck_ship = [len(ship.decks) for ship in ships]
        ship_counter = {item: numbers_deck_ship.count(item)
                        for item in set(numbers_deck_ship)}
        if ship_counter[1] != 4:
            print("There should be 4 single-deck ships")
        if ship_counter[2] != 3:
            print("There should be 3 double-deck ships")
        if ship_counter[3] != 2:
            print("There should be 2 three-deck ships")
        if ship_counter[4] != 1:
            print("There should be 1 four-deck ship")
        unavailable_cells = []
        for ship in ships:
            for cell in ship.decks:
                if (cell.row, cell.column) in unavailable_cells:
                    print("Ships shouldn't be located "
                          "in the neighboring cells")
            for cell in ship.decks:
                for ro in range(3):
                    for col in range(3):
                        place = (cell.row - 1 + ro, cell.column - 1 + col)
                        if place not in unavailable_cells:
                            unavailable_cells.append(place)


if __name__ == "__main__":
    boats = [
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]

    battle_ship = Battleship(boats)
    battle_ship.print_field()
    print(
        battle_ship.fire((0, 4)),  # Miss!
        battle_ship.fire((0, 3)),  # Hit!
        battle_ship.fire((0, 2)),  # Hit!
        battle_ship.fire((0, 1)),  # Hit!
        battle_ship.fire((0, 0)),  # Sunk!
    )
    battle_ship.print_field()
