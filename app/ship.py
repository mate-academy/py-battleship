from app.deck import Deck


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for cor in range(start[1], end[1] + 1):
                deck = Deck(start[0], cor)
                self.decks.append(deck)
        else:
            for cor in range(start[0], end[0] + 1):
                deck = Deck(cor, start[1])
                self.decks.append(deck)

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        count_of_fall_deck = 0

        for deck in self.decks:
            if deck.is_alive is False:
                count_of_fall_deck += 1

        if count_of_fall_deck == len(self.decks):
            self.is_drowned = True
