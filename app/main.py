class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int], end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.decks = []
        self.start = start
        self.end = end
        (row1, column1) = start
        (row2, column2) = end
        if row1 == row2:
            for column in range(min(column1, column2),
                                max(column1, column2) + 1):
                self.decks.append(Deck(row1, column, not is_drowned))
        elif column1 == column2:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, column1, not is_drowned))
        else:
            raise ValueError("Decks are diagonal")
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        try:
            goal_deck = next(deck for deck in self.decks
                             if deck.row == row and deck.column == column)
            return goal_deck
        except StopIteration:
            return None

    def fire(self, row: int, column: int) -> str:
        change_deck = self.get_deck(row, column)
        if change_deck is None or not change_deck.is_alive:
            return "Miss!"
        change_deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.field = {}
        ships_created = []
        for ship_like in ships:
            if isinstance(ship_like, Ship):
                ship = ship_like
            else:
                start, end = ship_like
                ship = Ship(start, end)
            ships_created.append(ship)
            (row1, column1) = ship.start
            (row2, column2) = ship.end
            if row1 == row2:
                for column in range(min(column1, column2),
                                    max(column1, column2) + 1):
                    self.field[(row1, column)] = ship
            elif column1 == column2:
                for row in range(min(row1, row2), max(row1, row2) + 1):
                    self.field[(row, column1)] = ship
        self._validate_field(ships_created)

    def _validate_field(self, ships: list[Ship]) -> None:
        if len(ships) != 10:
            raise ValueError("The length of the ships must be equal to 10.")
        ship_lengths = {4: 0, 3: 0, 2: 0, 1: 0}
        for ship in ships:
            (row1, column1) = ship.start
            (row2, column2) = ship.end
            length = abs(row2 - row1) + abs(column2 - column1) + 1
            ship_lengths[length] += 1
        if ship_lengths[4] != 1:
            raise ValueError("There should be 1 four-deck ship.")
        if ship_lengths[3] != 2:
            raise ValueError("There should be 2 three-deck ships.")
        if ship_lengths[2] != 3:
            raise ValueError("There should be 3 double-deck ships.")
        if ship_lengths[1] != 4:
            raise ValueError("There should be 4 single-deck ships.")
        neighbor_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for (row, column), ship in self.field.items():
            for delta_row, delta_column in neighbor_offsets:
                neighboor_row = row + delta_row
                neighboor_column = column + delta_column
            neighbor_ship = self.field.get((neighboor_row, neighboor_column))
            if neighbor_ship is not None and neighbor_ship != ship:
                raise ValueError(
                    f"Ships can't be adjacent (even diagonally): "
                    f"{(row, column)} touches "
                    f"{(neighboor_row, neighboor_column)}"
                )

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        return ship.fire(*location)

    def print_field(self) -> None:
        for row in range(10):
            rows = []
            for column in range(10):
                if (row, column) not in self.field:
                    rows.append("~")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        rows.append("x")
                    elif not deck.is_alive:
                        rows.append("*")
                    else:
                        rows.append("□")
            print(" ".join(rows))
