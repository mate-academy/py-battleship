from app.deck import Deck


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.add_new_ship()

    def add_new_ship(self) -> None:
        if self.end[0] == self.start[0] and self.end[1] == self.start[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
        elif self.end[0] == self.start[0]:
            for cell in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], cell))
        elif self.end[1] == self.start[1]:
            for cell in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(cell, self.start[0]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if any([decks.is_alive for decks in self.decks]):
            pass
        else:
            self.is_drowned = True
