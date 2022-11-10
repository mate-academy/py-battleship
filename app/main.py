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
        self.decks = self.checking_decks()

    def checking_decks(self) -> list:
        return [(self.start[0], self.start[1] + i)
                if self.start[1] != self.end[1]
                else (self.start[0] + i, self.start[1])
                for i in range((self.end[1] - self.start[1] + 1)
                               + (self.end[0] - self.start[0]))]

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck == (row, column):
                self.fire(row, column)
                break

    def fire(self, row: int, column: int) -> None:
        deck_exemplar = Deck(row, column)
        if deck_exemplar.is_alive:
            deck_exemplar.is_alive = False
            self.decks.remove((row, column))
            if len(self.decks) == 0:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.ships = ships
        self.field = {}
        self.create_field()

    def create_field(self) -> None:
        for ship in self.ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[deck] = new_ship

    def fire(self, location: tuple) -> str:
        for key, value in self.field.items():
            if key == location:
                value.get_deck(location[0], location[1])
                if value.is_drowned:
                    return "Sunk!"
                elif Deck(location[0], location[1]).is_alive:
                    return "Hit!"
                return "Miss!"
        return "Miss!"
