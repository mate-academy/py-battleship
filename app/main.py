class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
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
        self.decks = self.make_decks_for_ship()
        self.is_drowned = is_drowned

    def make_decks_for_ship(self) -> list:
        decks = []
        if self.start[0] == self.end[0]:
            # Ship is oriented horizontally
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            # Ship is oriented vertically
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck:
            target_deck.is_alive = False
            self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self,
                 ships: list
                 ) -> None:
        self.ships = ships
        self.field = self.making_ships()

    def making_ships(self) -> dict:
        field = {}
        for ship in self.ships:
            ship1 = Ship(ship[0], ship[1])
            for point in ship1.decks:
                field[(point.row, point.column)] = ship1
        return field

    def fire(self,
             location: tuple
             ) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
