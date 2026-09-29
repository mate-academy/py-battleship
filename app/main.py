class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.decks: list[Deck] = self._create_deck()

    def _create_deck(self) -> list[Deck]:
        """Private method to create the deck"""
        start_row, start_col = self.start
        end_row, end_col = self.end
        min_row, max_row = min(start_row, end_row), max(start_row, end_row)
        min_col, max_col = min(start_col, end_col), max(start_col, end_col)

        return [
            Deck(row, col)
            for row in range(min_row, max_row + 1)
            for col in range(min_col, max_col + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        """Find the corresponding deck in the list"""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        """Change the `is_alive` status of the deck
        And update the `is_drowned` value if it's needed"""
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = self._create_field(ships)
        self._validate_field()

    @staticmethod
    def _create_field(ships: list[tuple]) -> dict:
        """Private method to create the field"""
        field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        return field

    def _validate_field(self) -> None:
        """Private method to validate the field"""
        expected_ships = {1: 4, 2: 3, 3: 2, 4: 1}
        ships_count = {}

        ship_list = set(self.field.values())

        for ship in ship_list:
            ships_count[len(ship.decks)] = (
                ships_count.get(len(ship.decks), 0) + 1
            )

        if expected_ships != ships_count:
            raise ValueError("Invalid ship count:\n"
                             "there should be 4 single-deck ships;\n"
                             "there should be 3 double-deck ships;\n"
                             "there should be 2 three-deck ships;\n"
                             "there should be 1 four-deck ship.")

        for ship in ship_list:
            for deck in ship.decks:
                for row_offset in range(-1, 2):
                    for column_offset in range(-1, 2):
                        if (row_offset, column_offset) == (0, 0):
                            continue

                        neighbor_coordinates = (
                            deck.row + row_offset,
                            deck.column + column_offset
                        )
                        neighbor_ship = self.field.get(neighbor_coordinates)

                        if (neighbor_ship is not None
                                and neighbor_ship is not ship):
                            raise ValueError("Ships shouldn't be located in "
                                             "the neighboring cells "
                                             "(even if cells are neighbors "
                                             "by diagonal)")

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is not None:
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            column_symbols = []
            for column in range(10):
                ship = self.field.get((row, column))

                if ship is None:
                    column_symbols.append("~")
                elif ship.is_drowned:
                    column_symbols.append("x")
                elif not ship.get_deck(row, column).is_alive:
                    column_symbols.append("*")
                else:
                    column_symbols.append("\u25A1")

            print(" ".join(column_symbols))
