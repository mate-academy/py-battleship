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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            self.decks = [Deck(start[0], col)
                          for col in range(start[1], end[1] + 1)]
        elif start[1] == end[1] and start[0] != end[0]:
            self.decks = [Deck(row, start[1])
                          for row in range(start[0], end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = ships
        self._validate_field()

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field:
                    print("~", end=" ")
                ship = self.field.get((row, col))
                if ship:
                    if ship.is_drowned:
                        print("x", end=" ")
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        print(u"\u25A1", end=" ")
                    elif not deck.is_alive and not ship.is_drowned:
                        print("*", end=" ")
            print()

    def _validate_field(self) -> None:
        total_ships = len(self.ships)
        single_deck = double_deck = three_deck = four_deck = 0

        for start, end in self.ships:
            rows = set(range(start[0], end[0] + 1))
            columns = set(range(start[1], end[1] + 1))

            if len(rows) == 1 and len(columns) == 1:
                single_deck += 1
            elif len(rows) == 2 or len(columns) == 2:
                double_deck += 1
            elif len(rows) == 3 or len(columns) == 3:
                three_deck += 1
            elif len(rows) == 4 or len(columns) == 4:
                four_deck += 1

        if (total_ships != 10
                or single_deck != 4
                or double_deck != 3
                or three_deck != 2
                or four_deck != 1):
            raise ValueError("Invalid ship configuration")
