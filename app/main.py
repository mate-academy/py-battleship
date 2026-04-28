class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"

class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = None
        self.initialize_decks()

    def initialize_decks(self) -> None:
        self.decks = {}
        if self.start == self.end:
            self.decks[self.start] = Deck(row=self.start[0], column=self.start[1])

        elif self.start[0] == self.end[0]:
            for current_el in (range(self.start[1], self.end[1] + 1)):
                self.decks[(self.start[0], current_el)] = Deck(row=self.start[0], column=current_el)

        elif self.start[1] == self.end[1]:
            for  current_el in range(self.start[0], self.end[0] + 1):
                self.decks[(current_el, self.end[0])] = Deck(row=current_el, column=self.end[0])


    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        if self.check_is_drowned():
            self.is_drowned = True

    def check_is_drowned(self) -> bool:
        return not any(deck.is_alive for deck in self.decks.values())

    def __repr__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"

class Battleship:
    def __init__(self, ships:list) -> None:
        self.ships = [(Ship(start=ship[0], end=ship[1])) for ship in ships]
        self.field = {}
        self.initialize_field()

    def initialize_field(self) -> None:
        for ship in self.ships:
            for r_ship_deck, c_ship_deck in ship.decks.keys():
                self.field[(r_ship_deck, c_ship_deck)] = ship


    def fire(self, location: tuple) -> str:
        r, c = location
        if (r, c) in self.field:
            ship = self.field[r, c]
            ship.fire(r, c)
            if ship.is_drowned:
               return "Sunk!"
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        return f"Battleship({self.ships})"
