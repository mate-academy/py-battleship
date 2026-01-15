class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
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
        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field = {}
        for ship in ships:
            my_ship = Ship(ship[0], ship[1])
            for deck in my_ship.decks:
                self.field[(deck.row, deck.column)] = my_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
