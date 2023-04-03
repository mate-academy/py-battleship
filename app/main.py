from typing import Union


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.decks = self.create_decks()
        self.is_drowned = False

    def create_decks(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], column))
        else:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if not any([deck.is_alive for deck in self.decks]):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}
        self._buttlefield = [["~" for _ in range(10)] for _ in range(10)]

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def _buttlefield(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    self._buttlefield[deck.row][deck.column] = "Х"
                elif not deck.is_alive:
                    self._buttlefield[deck.row][deck.column] = "х"
                else:
                    self._buttlefield[deck.row][deck.column] = "*"

    def _validate_field(self) -> Union[None, Exception]:
        if len(self.field) != 10:
            Exception("You ought to create 10 ships")
            check_ships = [len(ship.decks) for ship in self.field.values()]
            if check_ships.count(1) != 4:
                Exception("There should be 4 1-deck ships!")
            if check_ships.count(2) != 3:
                Exception("There should be 3 2-deck ships!")
            if check_ships.count(3) != 2:
                Exception("There should be 2 2-deck ships!")
            if check_ships.count(4) != 1:
                Exception("There should be only one 1-deck ship!")
        for ship in self.field.values():
            for deck in ship.decks:
                for row, column in (deck[0] - 1, deck[1] + 2):
                    if Deck(row, column) not in ship.decks:
                        Exception("deck shouldn't border other ship's deck")
