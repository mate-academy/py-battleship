from app.deck import Deck


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> bool:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            for y_coord in range(min(y1, y2), max(y1, y2) + 1):
                self.decks.append(Deck(x1, y_coord))
        else:
            for x_coord in range(min(x1, x2), max(x1, x2) + 1):
                self.decks.append(Deck(x_coord, y1))

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)

        if not deck:
            return False

        if not deck.is_alive:
            return False

        deck.is_alive = False

        self.is_drowned = all(not d.is_alive for d in self.decks)

        return True
