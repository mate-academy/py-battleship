class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.shape = u"\u25A1"

    def __eq__(self, other: tuple) -> bool:
        return other == (self.row, self.column)


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = self.ship(start, end)
        self.is_drowned = is_drowned

    def __len__(self) -> int:
        return len(self.decks)

    @staticmethod
    def ship(start: tuple, end: tuple) -> list:
        if start[0] == end[0]:
            return [
                Deck(start[0], start[1] + i)
                for i in range(end[1] - start[1] + 1)
            ]
        if start[1] == end[1]:
            return [
                Deck(start[0] + i, start[1])
                for i in range(end[0] - start[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (row, column) == deck:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        deck.shape = "*"
        if not any(deck_.is_alive for deck_ in self.decks):
            self.is_drowned = True
            for deck in self.decks:
                deck.shape = "x"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship:
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for column in range(0, 10):
                if ship := self.field.get((row, column)):
                    print(ship.get_deck(row, column).shape, end="    ")
                else:
                    print("~", end="    ")
            print()
