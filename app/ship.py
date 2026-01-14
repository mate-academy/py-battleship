from app.deck import Deck


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned:
            bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            self.update_is_drowned()
            return self.is_drowned
        return False

    def update_is_drowned(self) -> None:
        self.is_drowned = all(not deck.is_alive for deck in self.decks)
