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

    def get_deck(self, row: int, column: int) -> None:
        # Find the corresponding deck in the list
        pass

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def print_field(self) -> None:
        list_decks = []
        for ship in self.field.values():
            for deck in ship.decks:
                list_decks.append((deck.row, deck.column))
        for row in range(10):
            for column in range(10):
                if (row, column) in list_decks:
                    print(u"\u25A1    ", end="")
                else:
                    print("~    ", end="")

            print("\n")

    def fire(self, location: tuple) -> str:
        bom = False
        for ship in self.field.values():
            if not ship.is_drowned:
                list_decks = []
                counter = 0
                for deck in ship.decks:
                    list_decks.append(deck)
                    if deck.is_alive:
                        counter += 1
                    if (deck.row, deck.column) == location:
                        bom = True
                        deck.is_alive = False
                        counter -= 1
                if bom:
                    if counter == 0:
                        return "Sunk!"
                    if counter > 0:
                        return "Hit!"
        return "Miss!"
