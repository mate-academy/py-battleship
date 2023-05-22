from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.is_drowned = is_drowned
        self.decks = []
        current_point = [start[0], start[1]]
        while current_point[0] != end[0]:
            self.decks.append(Deck(current_point[0], current_point[1]))
            current_point[0] += 1
        while current_point[1] != end[1]:
            self.decks.append(Deck(current_point[0], current_point[1]))
            current_point[1] += 1
        self.decks.append(Deck(current_point[0], current_point[1]))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck

    def fire(self, row: int, column: int) -> str:
        current_deck = self.get_deck(row, column)
        if current_deck.is_alive:
            current_deck.is_alive = False
            self.is_drowned = not any(deck.is_alive for deck in self.decks)
            if self.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            ship_instance = Ship(ship[0], ship[1])
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            return self.field[location].fire(location[0], location[1])
        else:
            return "Miss!"
