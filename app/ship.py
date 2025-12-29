from dataclasses import dataclass, field

from app.deck import Deck


@dataclass
class Ship:
    fleet = []

    start: tuple
    end: tuple
    alive_decks: int = field(init=False)
    count_of_decks: int = field(init=False)
    decks: list = field(default_factory=list)
    is_drowned: bool = False

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("the coordinate order is incorrect")
        if (self.start[0] != self.end[0]) and (self.start[1] != self.end[1]):
            raise ValueError(
                "The ship must be either vertical or horizontal,"
                " x or(and) y coordinates must be the same")
        list_of_decks = []
        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                list_of_decks.append(Deck(row, column))
        self.decks = list_of_decks
        self.alive_decks = len(self.decks)
        self.count_of_decks = len(list_of_decks)
        self.__class__.fleet.append(self)

    def __repr__(self) -> str:
        return f"ship({self.start}, {self.end})"

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck.is_alive

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                self.alive_decks -= 1
                if self.alive_decks == 0:
                    self.is_drowned = True
