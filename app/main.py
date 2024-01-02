from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = [
            Deck(row, col) for row, col in self._get_coordinates(start, end)
        ]
        self.is_drowned = is_drowned

    def _get_coordinates(self,
                         start: Tuple[int, int],
                         end: Tuple[int, int]) -> List[Tuple[int, int]]:
        if start[0] == end[0]:  # horizont
            return [(start[0], col) for col in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:  # Vert
            return [(row, start[1]) for row in range(start[0], end[0] + 1)]
        else:
            raise ValueError("Invalid ship placement")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {}
        for ship_coordinates in ships:
            ship = Ship(*ship_coordinates)
            for coord in self._get_coordinates(ship):
                self.field[coord] = ship

    def _get_coordinates(self, ship: Ship) -> List[Tuple[int, int]]:
        return [(deck.row, deck.column) for deck in ship.decks]

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            deck.is_alive = False
            if all(not d.is_alive for d in ship.decks):
                ship.is_drowned = True
                return "Sunk!"
            return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(*location)
                    if not deck.is_alive:
                        print("x", end=" ")
                    elif not ship.is_drowned:
                        print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")

            print()

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValueError
        number_of_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.field.values():
            size = len(ship.decks)
            if size not in number_of_ships:
                raise ValueError
            else:
                number_of_ships[size] += 1

        if number_of_ships != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError

        for coord1, ship1 in self.field.items():
            for coord2, ship2 in self.field.items():
                if ship1 != ship2 and self._are_neighbors(coord1, coord2):
                    raise ValueError

    def _are_neighbors(self,
                       coord1: Tuple[int, int],
                       coord2: Tuple[int, int]) -> bool:
        row1, col1 = coord1
        row2, col2 = coord2
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1
