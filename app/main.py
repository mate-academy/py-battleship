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
        self.is_drowned = is_drowned
        length = abs(start[0] - end[0]) + abs(start[1] - end[1]) + 1
        self.decks = []
        for i in range(length):
            if start[0] == end[0]:
                deck = Deck(start[0], start[1] + i)
            else:
                deck = Deck(start[0] + i, start[1])
            self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[(tuple[int, int], tuple[int, int])]
    ) -> None:
        self.ships = [Ship(start=ship[0], end=ship[1]) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        print("x", end="  ")
                    else:
                        if ship.get_deck(row, column).is_alive:
                            print(u"\u25A1", end="  ")
                        else:
                            print("*", end="  ")
                else:
                    print("~", end="  ")
            print()

    def _validate_field(self) -> None:
        n_ships = len(self.ships)
        if n_ships != 10:
            raise ValueError(f"Wrong number of ships: {n_ships}")
        decks_len = [0, 0, 0, 0]
        for ship in self.ships:
            len_ship = len(ship.decks)
            for i in range(1, 5):
                if len_ship == i:
                    decks_len[i - 1] += 1
        for i, count in enumerate(decks_len, start=1):
            if decks_len[i - 1] != count:
                raise ValueError(
                    f"Wrong number of {i}-deck ships: {decks_len[i - 1]}"
                )
