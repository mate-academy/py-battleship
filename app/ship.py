from app.deck import Deck


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = []
        self.decks_cells = set()
        self.set_decks()

        self.decks_with_margin_cells = set()
        self.set_decks_with_margin_cells()

    def set_decks(self) -> None:
        if self.start[0] != self.end[0]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))
                self.decks_cells.add((i, self.start[1]))

        if self.start[1] != self.end[1]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
                self.decks_cells.add((self.start[0], i))

        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.start[1]))
            self.decks_cells.add((self.start[0], self.start[1]))

    def set_decks_with_margin_cells(self) -> None:
        for deck in self.decks:
            if deck.row == 0 and deck.column == 0:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column + 1),
                ])
            elif deck.row == 0 and deck.column == 9:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                    (deck.row + 1, deck.column),
                ])
            elif deck.row == 9 and deck.column == 0:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                ])
            elif deck.row == 9 and deck.column == 9:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                ])
            elif (
                    deck.row == 0
                    and deck.column != 0
                    and deck.column != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column + 1),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                ])
            elif (
                    deck.row == 9
                    and deck.column != 0
                    and deck.column != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row, deck.column - 1),
                    (deck.row - 1, deck.column - 1),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                ])
            elif (
                    deck.column == 0
                    and deck.row != 0
                    and deck.row != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column + 1),
                    (deck.row + 1, deck.column),
                ])
            elif (
                    deck.column == 9
                    and deck.row != 0
                    and deck.row != 9
            ):
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                    (deck.row + 1, deck.column - 1),
                    (deck.row + 1, deck.column),
                ])
            else:
                self.decks_with_margin_cells.update([
                    (deck.row, deck.column),
                    (deck.row - 1, deck.column),
                    (deck.row - 1, deck.column + 1),
                    (deck.row, deck.column + 1),
                    (deck.row + 1, deck.column + 1),
                    (deck.row + 1, deck.column),
                    (deck.row + 1, deck.column - 1),
                    (deck.row, deck.column - 1),
                    (deck.row - 1, deck.column - 1),
                ])

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True