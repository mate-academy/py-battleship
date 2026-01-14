class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[1] != end[1]:
            for index in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], index))
        elif start[0] != end[0]:
            for index in range(start[0], end[0] + 1):
                self.decks.append(Deck(index, end[1]))
        elif start[1] == end[1] and start[0] == end[0]:
            for index in range(start[0], end[0] + 1):
                self.decks.append(Deck(index, end[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(start=ship_start, end=ship_end)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    self.field[(deck.row, deck.column)].append(ship)
                else:
                    self.field[(deck.row, deck.column)] = [ship]
        self.ships = ships

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ships_in_location = self.field[location]
            for ship in ships_in_location:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
