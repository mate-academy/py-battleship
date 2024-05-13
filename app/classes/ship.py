import numpy
import math

from app.classes.deck import Deck


class Ship:
    ship_set = {
        0: None,
        1: "single-deck ship",
        2: "double-deck ships",
        3: "three-deck ships",
        4: "four-deck ships",
    }

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self._init_decks(start, end)

    @classmethod
    def _init_decks(cls, start: tuple, end: tuple) -> tuple:
        length = int(abs(math.dist(start, end) + 1))
        coord_decks = list(
            zip(
                numpy.linspace(start[0], end[0], length, dtype=int),
                numpy.linspace(start[1], end[1], length, dtype=int)
            )
        )
        return [Deck(*deck) for deck in coord_decks]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.col == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            deck._sign = u"\u00D7"
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            for deck in self.decks:
                deck._sign = u"\u2620"
