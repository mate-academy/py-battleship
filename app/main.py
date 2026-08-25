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
        self.decks = []
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        if start_row != end_row and start_column != end_column:
            raise ValueError("Ship should be horizontal or vertical.")

        if start_row == end_row:
            for column in range(
                    min(start_column, end_column),
                    max(start_column, end_column) + 1
            ):
                self._validate_coordinate(start_row, column)
                self.decks.append(Deck(start_row, column))
        else:
            for row in range(
                    min(start_row, end_row),
                    max(start_row, end_row) + 1
            ):
                self._validate_coordinate(row, start_column)
                self.decks.append(Deck(row, start_column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        self.is_drowned = all(not deck.is_alive for deck in self.decks)

    def _validate_coordinate(self, row: int, column: int) -> None:
        if not 0 <= row <= 9 or not 0 <= column <= 9:
            raise ValueError("Ship coordinates should be from 0 to 9.")


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}

        for ship_coordinates in ships:
            start, end = ship_coordinates
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                location = (deck.row, deck.column)

                if location in self.field:
                    raise ValueError("Ships shouldn't overlap.")

                self.field[location] = ship

        self._validate_field()

    def fire(
            self,
            location: tuple
    ) -> str:
        if location not in self.field:
            return "Miss!"

        row, column = location
        ship = self.field[location]
        deck = ship.get_deck(row, column)

        if not deck.is_alive:
            return "Miss!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            field_row = []

            for column in range(10):
                location = (row, column)

                if location not in self.field:
                    field_row.append("~")
                    continue

                ship = self.field[location]

                if ship.is_drowned:
                    field_row.append("x")
                    continue

                deck = ship.get_deck(row, column)

                if deck.is_alive:
                    field_row.append("\u25A1")
                else:
                    field_row.append("*")

            print("\t".join(field_row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There should be exactly 10 ships.")

        ship_lengths = [len(ship.decks) for ship in self.ships]

        if ship_lengths.count(1) != 4:
            raise ValueError("There should be 4 single-deck ships.")

        if ship_lengths.count(2) != 3:
            raise ValueError("There should be 3 double-deck ships.")

        if ship_lengths.count(3) != 2:
            raise ValueError("There should be 2 three-deck ships.")

        if ship_lengths.count(4) != 1:
            raise ValueError("There should be 1 four-deck ship.")

        self._validate_ships_are_not_neighbors()

    def _validate_ships_are_not_neighbors(self) -> None:
        for first_ship in self.ships:
            for second_ship in self.ships:
                if first_ship is second_ship:
                    continue

                for first_deck in first_ship.decks:
                    for second_deck in second_ship.decks:
                        row_difference = abs(first_deck.row - second_deck.row)
                        column_difference = abs(
                            first_deck.column - second_deck.column
                        )

                        if row_difference <= 1 and column_difference <= 1:
                            raise ValueError(
                                "Ships shouldn't be located "
                                "in neighboring cells."
                            )
