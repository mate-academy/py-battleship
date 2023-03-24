class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:

        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.create_deck()

    def create_deck(self) -> None:
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.end[1]))

        elif self.start[0] != self.end[0]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[0]))

        elif self.start[1] != self.end[1]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.change_is_drowned()

    def change_is_drowned(self) -> None:
        self.is_drowned = not any(dec.is_alive for dec in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            boat = Ship(ship[0], ship[1])
            for deck in boat.decks:
                self.field[(deck.row, deck.column)] = boat

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
