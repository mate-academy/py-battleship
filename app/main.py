class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Deck(start={self.row}, end={self.column})"

    def __repr__(self) -> str:
        return str(self)


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
        self.decks = self.get_all_decks()

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            alive_decks = [deck for deck in self.decks if deck.is_alive]
            if alive_decks:
                return "Hit!"
            self.is_drowned = True
            return "Sunk!"

    def get_all_decks(self) -> tuple:
        x_direction = abs(self.start[0] - self.end[0])
        y_direction = abs(self.start[1] - self.end[1])

        if x_direction:
            return [
                Deck(self.start[0] + step, self.start[1])
                for step in range(x_direction + 1)
            ]
        elif y_direction:
            return [
                Deck(self.start[0], self.start[1] + step)
                for step in range(y_direction + 1)
            ]
        else:
            return [Deck(self.start[0], self.start[1])]

    def __str__(self) -> str:
        return f"Ship(start={self.start}, end={self.end})"

    def __repr__(self) -> str:
        return str(self)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.area = [["~"] * 10 for _ in range(10)]
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

        self._make_battle_area()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            value = ship.fire(*location)
            if value:
                return value
        return "Miss!"

    def print_field(self) -> None:
        self._make_battle_area()
        print("Battleship:")
        for row in self.area:
            print(*row)

    def _make_battle_area(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    self.area[deck.row][deck.column] = "x"
                elif not deck.is_alive:
                    self.area[deck.row][deck.column] = "*"
                else:
                    self.area[deck.row][deck.column] = u"\u25A1"
