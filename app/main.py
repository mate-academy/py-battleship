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
        if start[0] != end[0] and start[1] != end[1]:
            raise ValueError("Ship must be placed horizontally or vertically!")
        for coord in (start, end):
            if not (0 <= coord[0] <= 9 and 0 <= coord[1] <= 9):
                raise ValueError("Ship coordinates must be between 0 and 9!")
        if start[0] == end[0]:
            row = start[0]
            col_start = min(start[1], end[1])
            col_end = max(start[1], end[1])
            self.decks = [Deck(row, c) for c in range(col_start, col_end + 1)]
        else:
            col = start[1]
            row_start = min(start[0], end[0])
            row_end = max(start[0], end[0])
            self.decks = [Deck(r, col) for r in range(row_start, row_end + 1)]

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.column == column and deck.row == row:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck_shot = self.get_deck(row, column)
        if deck_shot is None:
            return
        deck_shot.is_alive = False
        count = 0
        for deck in self.decks:
            if deck.is_alive is False:
                count += 1
        if len(self.decks) == count:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship_tuple in ships:
            ship_obj = Ship(ship_tuple[0], ship_tuple[1])
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
