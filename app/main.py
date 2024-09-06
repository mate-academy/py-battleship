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
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        elif start[1] == end[1]:
            self.decks = [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            decks = tuple(
                [(deck.row, deck.column) for deck in new_ship.decks]
            )
            self.field[decks] = new_ship

    def fire(self, location: tuple) -> str:
        for decks, ship in self.field.items():
            if location in decks:
                return ship.fire(location[0], location[1])

        return "Miss!"
