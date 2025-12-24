from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        coordinates = self.get_ship_coordinates(start, end)
        self.decks = [Deck(row, column) for row, column in coordinates]
        self.is_drowned = is_drowned

    def get_ship_coordinates(self, start: Tuple[int, int],
                             end: Tuple[int, int]) -> List[Tuple[int, int]]:
        coordinates = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                coordinates.append((start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                coordinates.append((row, start[1]))
        return coordinates

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
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
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        self._validate_field(ships)
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def _validate_field(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        if len(ships) != 10:
            raise ValueError("The total number of ships should be 10.")

        ship_lengths = [
            len(self.get_ship_coordinates(start, end))
            for start, end in ships
        ]
        if (ship_lengths.count(1) != 4
                or ship_lengths.count(2) != 3
                or ship_lengths.count(3) != 2
                or ship_lengths.count(4) != 1):
            raise ValueError("Invalid number of ships of each type.")

        for i in range(len(ships)):
            for j_j in range(i + 1, len(ships)):
                if self.are_ships_neighbors(ships[i], ships[j_j]):
                    raise ValueError(
                        "Ships should not be located in neighboring cells."
                    )

    def are_ships_neighbors(
            self,
            ship1: Tuple[Tuple[int, int], Tuple[int, int]],
            ship2: Tuple[Tuple[int, int], Tuple[int, int]]
    ) -> bool:
        for coord1 in self.get_ship_coordinates(ship1[0], ship1[1]):
            for coord2 in self.get_ship_coordinates(ship2[0], ship2[1]):
                if (abs(
                        coord1[0] - coord2[0]) <= 1
                        and abs(coord1[1] - coord2[1]) <= 1):
                    return True
        return False

    def get_ship_coordinates(
            self,
            start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        coordinates = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                coordinates.append((start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                coordinates.append((row, start[1]))
        return coordinates

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
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
                            print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            print()
