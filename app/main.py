class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.decks = [Deck(row, column)
                      for column in range(start[1], end[1] + 1)
                      for row in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = True
        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def print_field(self) -> None:
        list_decks = {}
        for ship in self.field.values():
            for deck in ship.decks:
                list_decks[(deck.row, deck.column)] = deck.is_alive
        for row in range(10):
            for column in range(10):
                if (row, column) in list_decks.keys():
                    if list_decks[(row, column)] is True:
                        print(u"\u25A1    ", end="")
                    else:
                        print("x    ", end="")
                else:
                    print("~    ", end="")
            print("\n")

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if not ship.is_drowned:
                deck = ship.get_deck(location[0], location[1])
                if deck is not None:
                    ship.fire(deck.row, deck.column)
                    if ship.is_drowned:
                        return "Sunk!"
                    else:
                        return "Hit!"
        return "Miss!"
