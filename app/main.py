from typing import Any


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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks, self.map = self._create_deck()

    def _create_deck(self) -> Any:
        deck_list = []
        deck_mapping = {}

        if self.start == self.end:
            deck = Deck(self.start[0], self.start[1], is_alive=True)
            deck_mapping[self.start] = self
            deck_list.append(deck)

        elif self.start[0] == self.end[0]:  # horizontal ship

            for index in range(self.end[1] - self.start[1] + 1):
                coordinates = (self.start[0], self.start[1] + index)
                deck = Deck(*coordinates, is_alive=True)
                deck_mapping[coordinates] = self
                deck_list.append(deck)

        elif self.start[1] == self.end[1]:  # vertical ship

            for index in range(self.end[0] - self.start[0] + 1):
                coordinates = (self.start[0] + index, self.start[1])
                deck = Deck(*coordinates, is_alive=True)
                deck_mapping[coordinates] = self
                deck_list.append(deck)
        return deck_list, deck_mapping

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if not deck:
            return "Miss!"
        deck.is_alive = False

        for status in self.decks:
            if status.is_alive:
                return "Hit!"

        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field: dict = {}

        for ship in ships:
            created_ship = Ship(ship[0], ship[1])
            self.field.update(created_ship.map)

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if not ship:
            return "Miss!"
        return ship.fire(*location)
