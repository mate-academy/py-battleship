class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, target: Deck) -> str:
        target.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])
        if self.is_drowned:
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for coords in ships:
            ship = Ship(*coords)
            self.field.update({tuple(
                [(deck.row, deck.column) for deck in ship.decks]
            ): ship})

    def fire(self, location: tuple) -> str:
        for coords, ship in self.field.items():
            if location in coords:
                return ship.fire(ship.get_deck(*location))
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                check = "~"
                for coords, ship in self.field.items():
                    if (row, column) in coords:
                        cell = ship.get_deck(row, column)
                        if cell.is_alive:
                            check = u"\u25A1"
                        else:
                            check = "X"
                print(check + "  ", end="")
            print("\n")

    def _validate_field(self) -> str:
        ships_by_decks = [len(key) for key in self.field.keys()]
        if ships_by_decks.count(1) != 4:
            return "Should be 4 single-deck ships"
        if ships_by_decks.count(2) != 3:
            return "Should be 3 double-deck ships"
        if ships_by_decks.count(3) != 2:
            return "Should be be 2 three-deck ships"
        if ships_by_decks.count(4) != 1:
            return "Should be 4 1 four-deck ship"

        restricted_area = []
        for ship in self.field.keys():
            for coords in ship:
                if coords in restricted_area:
                    return (
                        "Ships shouldn't be located in the \n"
                        "neighboring cells (even if cells \n"
                        "are neighbors by diagonal)")
                for restr_row in range(coords[0] - 1, coords[0] + 2):
                    for restr_column in range(coords[1] - 1, coords[1] + 2):
                        if (restr_row, restr_column) not in restricted_area:
                            restricted_area.append((restr_row, restr_column))
