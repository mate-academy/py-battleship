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
            is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))
        print([(deck.row, deck.column) for deck in self.decks])

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck is None:
            return "Miss!"

        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])

        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            deck = ship.get_deck(location[0], location[1])
            if deck is not None:
                result = ship.fire(location[0], location[1])
                self.print_field()
                return result

        self.print_field()
        return "Miss!"

    def print_field(self) -> None:
        matrix = []

        ship_cells = {}
        for ship in self.field.values():
            for deck in ship.decks:
                ship_cells[(deck.row, deck.column)] = {
                    "alive": deck.is_alive,
                    "drowned": ship.is_drowned
                }

        for rows in range(10):
            row = []
            for cols in range(10):
                cell = ship_cells.get((rows, cols))

                if cell is None:
                    row.append("~")
                else:
                    if cell["drowned"]:
                        row.append("x")
                    elif not cell["alive"]:
                        row.append("*")
                    else:
                        row.append(u"\u25A1")
            matrix.append(row)

        for row in matrix:
            print(*row)

    def _validate_field(self) -> None:
        required_num_of_ships = {1: 4, 2: 3, 3: 2, 4: 1}

        if len(self.field) != 10:
            raise ValueError("Field must contain exactly 10 ships.")

        ships_to_compare = {}
        for ship in self.field.values():
            size = len(ship.decks)
            ships_to_compare[size] = ships_to_compare.get(size, 0) + 1

        if ships_to_compare != required_num_of_ships:
            raise ValueError(
                f"Invalid ship composition: "
                f"{ships_to_compare}, expected {required_num_of_ships}"
            )

        all_decks = {
            (d.row, d.column)
            for ship in self.field.values()
            for d in ship.decks
        }
        for ship in self.field.values():
            for deck in ship.decks:
                rows, cols = deck.row, deck.column
                neighbors = [
                    (rows - 1, cols - 1),
                    (rows - 1, cols), (rows - 1, cols + 1),
                    (rows, cols - 1), (rows, cols + 1),
                    (rows + 1, cols - 1), (rows + 1, cols),
                    (rows + 1, cols + 1),
                ]
                for nr, nc in neighbors:
                    if (nr, nc) in all_decks:
                        is_same_ship = any(
                            (d.row, d.column) == (nr, nc)
                            for d in ship.decks
                        )
                        if not is_same_ship:
                            raise ValueError(
                                f"Ships cannot touch each other: "
                                f"deck {(rows, cols)} touches {(nr, nc)}"
                            )
