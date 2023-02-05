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
        self.decks = []
        self.is_drowned = is_drowned
        if start[0] != end[0]:
            index = 0
        else:
            index = 1

        for part_deck in range(
                min(start[index], end[index]),
                max(start[index], end[index]) + 1
        ):
            row = start[0] if index == 1 else part_deck
            column = start[1] if index == 0 else part_deck
            self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            for index in range(len(ship.decks)):
                self.field[(
                    ship.decks[index].row,
                    ship.decks[index].column
                )] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
