from typing import Optional, Tuple


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:

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
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            row = start[0]
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))

        elif start[1] == end[1]:
            col = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self,
                 row: int,
                 column: int
                 ) -> Optional[Deck]:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> str:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                if deck.is_alive:
                    deck.is_alive = False
                    if all(not d.is_alive for d in self.decks):
                        self.is_drowned = True
                        return "Sunk!"
                    else:
                        return "Hit!"
                else:
                    return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:

        self.field = {}
        self.ships = [Ship(start, end) for (start, end) in ships]
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(
            self,
            location: Tuple[int, int]
    ) -> str:

        row, column = location
        if (row, column) in self.field:
            ship = self.field[(row, column)]
            return ship.fire(row, column)
        else:
            return "Miss!"
