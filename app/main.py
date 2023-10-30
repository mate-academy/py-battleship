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

    def __getitem__(self, item: int) -> int:
        if item == 0:
            return self.row
        elif item == 1:
            return self.column


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool | None = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            start_point = start[1]
            end_point = end[1] + 1
            for column in range(start_point, end_point):
                self.decks.append(Deck(start[0], column))
        elif start[1] == end[1]:
            start_point = start[0]
            end_point = end[0] + 1
            for row in range(start_point, end_point):
                self.decks.append(Deck(row, end[1]))
        elif start[0] == end[0] and start[1] == end[1]:
            self.decks.append(Deck(start[0], end[0]))

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck[0] and column == deck[1]:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.decks.index(self.get_deck(row, column))
        self.decks[deck].is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.field = {}
        for data in ships:
            ship = Ship(data[0], data[1])
            for deck in ship.decks:
                self.field[(deck[0], deck[1])] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            if isinstance(self.field[location], Ship):
                self.field[location].fire(location[0], location[1])
                if not self.field[location].is_drowned:
                    return "Hit!"
                return "Sunk!"
        return "Miss!"
