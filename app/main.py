from typing import Union


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list:
        decks = list()

        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                deck = Deck(row, column)
                decks.append(deck)

        return decks

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if self.is_ship_drowned():
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def is_ship_drowned(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return False
        return True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = self.create_field(ships)

    def create_field(self, ships: list) -> dict:
        field = {}
        for ship in ships:
            start, end = ship
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                field[(deck.row, deck.column)] = new_ship
        return field

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        if ship.is_drowned:
                            print("x    ")
                        else:
                            print(u"\u25A1  ")
                    else:
                        print("*    ")
                else:
                    print("~    ")
            print()
