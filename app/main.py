from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, drown: bool = False) -> None:
        self.decks = []
        self.is_drowned = drown
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field.update({(deck.row, deck.column): new_ship})
        if not self._validate_field():
            print("Incorrect input list")

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        if self.field[location].fire(location[0], location[1]):
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        print("\n")
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field.keys():
                    print("~\t", end="")
                    continue
                if self.field[(row, col)].is_drowned:
                    print("x\t", end="")
                    continue
                deck = self.field[(row, col)].get_deck(row, col)
                if deck.is_alive:
                    print(u"\u25A1\t", end="")
                    continue
                print("*\t", end="")
            print("\n")

    def _validate_field(self) -> bool:
        ships = set(self.field.values())
        if not len(ships) == 10:
            return False
        single_deck = sum([1 for ship in ships if len(ship.decks) == 1]) == 4
        double_deck = sum([1 for ship in ships if len(ship.decks) == 2]) == 3
        three_deck = sum([1 for ship in ships if len(ship.decks) == 3]) == 2
        four_deck = sum([1 for ship in ships if len(ship.decks) == 4]) == 1
        if not all([single_deck, double_deck, three_deck, four_deck]):
            return False
        for ship in ships:
            for deck in ship.decks:
                for row in range(-1, 2):
                    for col in range(-1, 2):
                        near_row = deck.row + row
                        near_col = deck.column + col
                        if (near_row, near_col) in self.field.keys():
                            if self.field[(near_row, near_col)] != ship:
                                return False
        return True
