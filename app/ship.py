from app.build_decks import build_decks
from app.deck import Deck


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        # Create decks and save them to a list `self.decks`
        self.decks = build_decks(start, end)

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck is not None:
            target_deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
