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
        self.decks = [
            Deck(row_number, column_number)
            for row_number in range(start[0], end[0] + 1)
            for column_number in range(start[1], end[1] + 1)
        ]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False

    def check_if_ship_is_drowned(self) -> None:
        decks_is_alive = any(
            deck.is_alive
            for deck in self.decks
        )
        if not decks_is_alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.ships = [
            Ship(start, end)
            for (start, end) in ships
        ]
        self.field = self.cells_to_ship_reference()

    def cells_to_ship_reference(self) -> dict[tuple[int, int]: Ship]:
        return {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field.keys():
            ship = self.field.get(location)
            ship.fire(location[0], location[1])
            ship.check_if_ship_is_drowned()

            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"

        return "Miss!"

    def get_cell_status(self, row: int, column: int) -> str:
        for ship in self.ships:
            for deck in ship.decks:
                if (row, column) == (deck.row, deck.column):
                    if not deck.is_alive:
                        cell = "x"
                    elif ship.is_drowned:
                        cell = "*"
                    else:
                        cell = u"\u25A1"
                    return cell
        return "~"

    def print_field(self) -> None:
        for row in range(10):
            print(
                [
                    self.get_cell_status(row, column)
                    for column in range(10)
                ]
            )
