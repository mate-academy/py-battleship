from ast import List
import random


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_deck(self) -> tuple:
        return (self.row, self.column)


class Ship:

    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        self.decks = self._decks_generator(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: tuple, column: tuple) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: tuple, column: tuple):
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            decks_alive = list(filter(lambda x: x.is_alive == True, self.decks))
            if not decks_alive:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    @staticmethod
    def _decks_generator(start: tuple, end: tuple) -> list:
        start_row, end_row = start
        start_column, end_column = end
        if start_row == end_row:
            return [Deck(start_column, cell) for cell in range(start_column, end_column + 1)]
        return [Deck(start_row, row) for row in range(start_row, end_row + 1)]


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        self.fields = get_fields(ships)
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def get_fields(self, ships) -> dict:
