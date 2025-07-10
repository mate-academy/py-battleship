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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = []

        if start[0] == end[0]:
            row = start[0]
            start_col = min(start[1], end[1])
            end_col = max(start[1], end[1])
            for col in range(start_col, end_col + 1):
                self.decks.append(Deck(row, col))
        else:
            col = start[1]
            start_row = min(start[0], end[0])
            end_row = max(start[0], end[0])
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None | str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        return None


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = []

        for ship_coords in ships:
            ship = Ship(ship_coords[0], ship_coords[1])
            self.ships.append(ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_fields()

    def fire(self, location: tuple) -> tuple | str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            return result
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)

                    if ship.is_drowned:
                        line += "+ "
                    elif not deck.is_alive:
                        line += "* "
                    else:
                        line += "□ "
                else:
                    line += "~ "
            print(line)

    def _validate_fields(self) -> None:
        if len(self.ships) != 10:
            raise ValueError(
                f"Ships must have 10 ships not {len(self.ships)}"
            )

        ship_length = {}
        for ship in self.ships:
            length = len(ship.decks)
            ship_length[length] = ship_length.get(length, 0) + 1

        expected_ships = {1: 4, 2: 3, 3: 2, 4: 1}
        for length, count in expected_ships.items():
            if ship_length.get(length, 0) != count:
                raise ValueError(
                    f"Expected {count} ships of {length}, "
                    f"got {ship_length.get(length, 0)}"
                )
