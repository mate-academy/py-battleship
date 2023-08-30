from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: Tuple[int], end: Tuple[int], is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not every_deck.is_alive for every_deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

        if not self._validate_field():
            raise ValueError("Invalid data received! Check input data.")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            if deck.is_alive:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
            return "Miss!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(*location)
                    if ship.is_drowned:
                        print(" x ", end=" ")
                    elif deck.is_alive:
                        print(" \u25A1 ", end=" ")
                    else:
                        print(" * ", end=" ")
                else:
                    print(" ~ ", end=" ")
            print()

    def _validate_field(self) -> bool:
        ship_count = {1: 4, 2: 3, 3: 2, 4: 1}

        counts = {i: 0 for i in range(1, 5)}

        ships = set([ship for ship in self.field.values()])

        for ship in ships:
            ship_decks = len(ship.decks)
            if ship_decks in counts:
                counts[ship_decks] += 1
            else:
                return False

        if sum(counts.values()) != sum(ship_count.values()):
            return False

        return True
