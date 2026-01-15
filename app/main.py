from typing import List, Tuple, Optional


# Some comments
class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.decks: List[Deck] = []
        self.is_drowned: bool = False

        if start[0] == end[0]:
            for y_point in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], y_point))
        else:
            for x_point in range(start[0], end[0] + 1):
                self.decks.append(Deck(x_point, start[1]))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(
            self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []

        for ship_coords in ships:
            ship = Ship(*ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        # Check if the shot hit any ship
        if location in self.field:
            ship = self.field[location]
            hit_result = ship.fire(*location)

            if hit_result:
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        return "Miss!"
