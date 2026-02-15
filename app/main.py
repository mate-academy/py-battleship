from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.decks = []

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck:
            deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"

        return "Miss!"


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = [Ship(start, end) for start, end in ships]

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(*location)

        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    deck = self.field[(row, column)].get_deck(row, column)

                    if deck.is_alive:
                        print(u"\u25A1", end=" " * 3)
                        continue
                    elif not self.field[(row, column)].is_drowned:
                        print("*", end=" " * 3)
                        continue
                    print("x", end=" " * 3)
                    continue

                print("~", end=" " * 3)

            print("")
