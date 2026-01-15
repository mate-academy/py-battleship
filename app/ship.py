from app.deck import Deck


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks: list[Deck] = []
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return True
        return False
