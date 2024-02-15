class Deck:
    visible_symbol = u"\u25A1  "
    destroyed_symbol = "x  "

    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return self.visible_symbol if self.is_alive else self.destroyed_symbol


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks: list[Deck] = [
            Deck(row, column) for row, column in self._get_deck(start, end)
        ]
        self.is_drowned = is_drowned

    @staticmethod
    def _get_deck(start: tuple, end: tuple) -> list:
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            return [(x1, y) for y in range(
                min(y1, y2), max(y1, y2) + 1)]
        elif y1 == y2:
            return [(x, y1) for x in range(
                min(x1, x2), max(x1, x2) + 1)]

    def fire(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                if all(not deck.is_alive for deck in self.decks):
                    self.is_drowned = True
                return True
        return False


class Battleship:

    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships_on_the_field()

    def __str__(self) -> str:
        result = ""
        for row in self.field:
            for item in row:
                if isinstance(item, Deck):
                    result += str(item)
                else:
                    result += item + "  "
            result += "\n"
        return result

    def ships_on_the_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                x1, y1 = deck.row, deck.column
                self.field[x1][y1] = deck

    def fire(self, location: tuple) -> str:
        try:
            x1, y1 = location
            target = self.field[x1][y1]
            if isinstance(target, Deck):
                if target.is_alive:
                    for ship in self.ships:
                        if target in ship.decks:
                            ship.fire(x1, y1)
                            if ship.is_drowned:
                                return "Sunk!"
                    return "Hit!"
            return "Miss!"
        except IndexError:
            return "Invalid coordinates!"
