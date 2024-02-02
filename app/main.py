class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def create_decks_between_points(self, start: tuple, end: tuple) -> None:
        for i in range((end[0] - start[0]) + (end[1] - start[1]) + 1):
            if start[0] == end[0]:
                self.decks.append(Deck(start[0], start[1] + i))
            elif start[1] == end[1]:
                self.decks.append(Deck(start[0] + i, start[1]))

    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks_between_points(start, end)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def create_field(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])

    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field = {}
        self.create_field(ships)

    def fire(self, location: tuple) -> str:
        for key in self.field.keys():
            if (key[0][0] <= location[0] <= key[1][0]
                    and key[0][1] <= location[1] <= key[1][1]):
                self.field[key].fire(location[0], location[1])
                if self.field[key].is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
