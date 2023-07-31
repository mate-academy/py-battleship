from typing import Union


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: list,
            end: list,
            is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Union[list, None]:
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
    def __init__(self, ships: list) -> None:
        self._validate_field(ships)
        self.field = {}
        for ship in ships:
            start, end = ship
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            return result
        return "Miss!"

    def print_field(self) -> str:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        if ship.is_drowned:
                            print("x")
                        else:
                            print(u"\u25A1")
                    else:
                        print("*")
                else:
                    print("~")
            print()

    def _validate_field(self, ships: list) -> None:
        total_ships = len(ships)
        if total_ships != 10:
            raise ValueError("There should be exactly 10 ships.")

        single_deck = 0
        double_deck = 0
        three_deck = 0
        four_deck = 0

        for ship in ships:
            start, end = ship
            size = max(abs(start[0] - end[0]), abs(start[1] - end[1])) + 1
            if size == 1:
                single_deck += 1
            elif size == 2:
                double_deck += 1
            elif size == 3:
                three_deck += 1
            elif size == 4:
                four_deck += 1
            else:
                raise ValueError("Invalid ship size.")

        if (single_deck != 4
                or double_deck != 3
                or three_deck != 2
                or four_deck != 1):
            raise ValueError("Invalid number of ships of each size.")
