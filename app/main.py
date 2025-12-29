class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return "□" if self.is_alive else "x"


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.decks: list = []
        self.is_drowned: bool = False
        self.create_decks(start, end)

    def create_decks(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        self._place_ships(ships)

    def _place_ships(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            hit = ship.fire(location[0], location[1])
            if hit:
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
            return "Miss!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    deck = self.field[(row, col)].get_deck(row, col)
                    print(deck, end=" ")
                else:
                    print("~", end=" ")
            print()
