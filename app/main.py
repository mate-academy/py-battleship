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
            start: int,
            end: int,
            is_drowned: bool = False
    ) -> None:
        self.start_x, self.start_y = start
        self.end_x, self.end_y = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start_x == self.end_x:
            for y_coord in range(
                    min(self.start_y, self.end_y),
                    max(self.start_y, self.end_y) + 1):
                self.decks.append(Deck(self.start_x, y_coord))

        elif self.start_y < self.end_y:
            for x_coord in range(
                    min(self.start_x, self.end_x),
                    max(self.start_x, self.end_x) + 1):
                self.decks.append(Deck(x_coord, self.start_y))
        else:
            return

    def get_deck(
            self,
            row: int,
            column: int
    ) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            for _deck in self.decks:
                if _deck.is_alive is True:
                    return
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.ships = []
        self.field = {}
        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships.append(new_ship)

        for ship in self.ships:
            for deck in ship.decks:
                coord = (deck.row, deck.column)
                self.field[coord] = ship

    def fire(
            self,
            location: tuple
    ) -> str:
        if location not in self.field:
            return "Miss!"
        target_ship = self.field[location]
        target_ship.fire(*location)
        if target_ship.is_drowned:
            return "Sunk!"
        return "Hit!"
