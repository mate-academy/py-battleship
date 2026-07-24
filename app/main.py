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
        self.is_drowned = is_drowned
        start_row, start_col = start
        end_row, end_col = end

        self.decks = []

        if start_row == end_row:
            for column in range(start_col, end_col + 1):
                self.decks.append(Deck(start_row, column))
        else:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, start_col))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def _check_neighbours(self, deck: Deck, ship: Ship) -> None:
        for row_offset in range(-1, 2):
            for column_offset in range(-1, 2):
                if row_offset == 0 and column_offset == 0:
                    continue
                neighbour_row = deck.row + row_offset
                neighbour_column = deck.column + column_offset

                if (neighbour_row, neighbour_column) in self.field:
                    neighbour_ship = self.field[(neighbour_row,
                                                 neighbour_column)]

                    if neighbour_ship is not ship:
                        raise ValueError("Ships shouldn't be "
                                         "located in the neighbouring cells")

    def _validate_field(self) -> None:
        ships = set(self.field.values())

        if len(ships) != 10:
            raise ValueError("Total number of the ships should be 10")

        single_deck_count = sum(len(ship.decks) == 1 for ship in ships)
        double_deck_count = sum(len(ship.decks) == 2 for ship in ships)
        three_deck_count = sum(len(ship.decks) == 3 for ship in ships)
        four_deck_count = sum(len(ship.decks) == 4 for ship in ships)

        if single_deck_count != 4:
            raise ValueError("There should be 4 single-deck ships")

        if double_deck_count != 3:
            raise ValueError("There should be 3 double-deck ships")

        if three_deck_count != 2:
            raise ValueError("There should be 2 three-deck ships")

        if four_deck_count != 1:
            raise ValueError("There should be 1 four-deck ship")

        for ship in ships:
            for deck in ship.decks:
                self._check_neighbours(deck, ship)

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        row, column = location
        ship.fire(row, column)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) not in self.field:
                    print("~", end=" ")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)

                    if deck.is_alive:
                        print("□", end=" ")

                    elif not ship.is_drowned:
                        print("*", end=" ")

                    else:
                        print("x", end=" ")
            print()
