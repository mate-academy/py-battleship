from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(
            self, start: tuple[int], end: tuple[int], is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        self._create_ship(start, end)

    def _create_ship(self, start: tuple[int], end: tuple[int]) -> None:
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        alive_decks = [deck.is_alive for deck in self.decks]

        if any(alive_decks):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = tuple(Ship(*ship) for ship in self.ships)

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            if ship.get_deck(*location):
                return ship.fire(*location)

        return "Miss!"
