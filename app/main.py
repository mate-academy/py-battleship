class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        start_row, start_col = start
        end_row, end_col = end

        for r in range(min(start_row, end_row), max(start_row, end_row) + 1):
            for c in range(min(start_col, end_col), max(start_col, end_col) + 1):
                self.decks.append(Deck(r, c))

    def get_deck(self, row: int, column: int) -> "Deck | None":
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships_instances = []
        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships_instances.append(new_ship)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.ships_instances) != 10:
            raise ValueError("There must be exactly 10 ships")

        sizes = [len(ship.decks) for ship in self.ships_instances]
        if sorted(sizes) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Invalid ship sizes distribution")

        for ship in self.ships_instances:
            for deck in ship.decks:
                for r_offset in range(-1, 2):
                    for c_offset in range(-1, 2):
                        neighbor = (deck.row + r_offset, deck.column + c_offset)
                        if neighbor in self.field and self.field[neighbor] is not ship:
                            raise ValueError("Ships are too close to each other")

    def print_field(self) -> None:
        for r in range(10):
            row_str = ""
            for c in range(10):
                if (r, c) in self.field:
                    ship = self.field[(r, c)]
                    deck = ship.get_deck(r, c)
                    if deck.is_alive:
                        row_str += "□ "
                    else:
                        row_str += "x " if ship.is_drowned else "* "
                else:
                    row_str += ". "
            print(row_str.strip())
