class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.start[0] != self.end[0]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))
        else:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None:
            return AttributeError("Unknown deck")
        deck.is_alive = False
        if_all_ship_die = False
        for i in self.decks:
            if i.is_alive:
                if_all_ship_die = True
        if if_all_ship_die is False:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for i in range(len(ships)):
            if ships[i][0][0] != ships[i][1][0]:
                ship = Ship(ships[i][0], ships[i][1])
                for index in range(ships[i][0][0], ships[i][1][0] + 1):
                    self.field[(index, ships[i][1][1])] = ship
            else:
                ship = Ship(ships[i][0], ships[i][1])
                for index in range(ships[i][0][1], ships[i][1][1] + 1):
                    self.field[(ships[i][1][0], index)] = ship

    def fire(self, location: tuple) -> None:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
