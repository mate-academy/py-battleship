from app.deck import Deck


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False
                 ) -> None:
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def create_decks(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list:
        decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(row, column))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.check_if_drowned()

    def check_if_drowned(self) -> None:
        self.is_drowned = not any(deck for deck in self.decks if deck.is_alive)
