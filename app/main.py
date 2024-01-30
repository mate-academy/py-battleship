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
        self.decks = [Deck(row, col)
                      for row, col in self._get_coordinates(start, end)]
        self.is_drowned = is_drowned

    @classmethod
    def _get_coordinates(
            cls,
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        coordinates = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                coordinates.append((start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                coordinates.append((row, start[1]))
        return coordinates

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}

        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(location[0], location[1])
            if deck.is_alive:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        if ship.is_drowned:
                            print("x", end=" ")
                        else:
                            print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
