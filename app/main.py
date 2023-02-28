from typing import Dict, List, Tuple, Optional


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
            is_hit: bool = False,
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.is_hit = is_hit


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def __repr__(self) -> str:
        if not self.is_drowned:
            return " ".join([str(deck) for deck in self.decks])
        return " ".join(["x" for _ in self.decks])

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.check_drowned()

    def check_drowned(self) -> None:
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self._validate_field(ships)
        for ship in ships:
            ship_obj = Ship(start=ship[0], end=ship[1])
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj

    def _validate_field(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        if len(ships) != 10:
            raise ValueError("The total number of ships should be 10")

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            deck = ship.get_deck(*location)
            deck.is_alive = False
            if all(deck.is_alive is False for deck in ship.decks):
                ship.is_drowned = True
                return "Sunk!"
            deck.is_hit = True
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field:
                    print("~", end=" ")
                else:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if not deck.is_hit and not ship.is_drowned:
                        print("□", end=" ")
                    elif deck.is_hit and not ship.is_drowned:
                        print("*", end=" ")
                    else:
                        print("x", end=" ")
            print()
