class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"{self.row, self.column}"


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            for vertical in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], vertical))
        else:
            for horizontal in range(start[0], end[0] + 1):
                self.decks.append(Deck(horizontal, start[0]))

    def __repr__(self) -> str:
        return f"{self.decks}"

    def get_deck(self, row: int, column: int) -> object:
        for deck in self.decks:
            if str(deck) == str((row, column)):
                return deck

    def fire(self, row: int, column: int) -> None:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False

        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}

        for ship in ships:
            current_ship = Ship(ship[0], ship[1])
            for ceil in current_ship.decks:
                self.field[(ceil.row, ceil.column)] = current_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
