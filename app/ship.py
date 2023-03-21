class Ship:
    def __init__(self, start, end, is_drowned=False):
        """Create decks and save them to a list `self.decks`"""

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._all_decks_ship()

    def get_deck(self, row, column):
        """Find the corresponding deck in the list"""

        for deck in self.decks:
            if isinstance(deck, Deck) and \
                    deck.row == row and deck.column == column:
                return deck

    def _kill_deck(self, deck):
        """Change the `is_alive` status of the deck
        And update the `is_drowned` value if it's needed"""

        index_the_same_cord = self.decks.index(deck)
        self.decks[index_the_same_cord] = None
        deck.is_alive = False

    def _all_decks_ship(self):
        x, y = self.start
        x_end, y_end = self.end
        self.decks_ship = [Deck(x, y)]
        while x != x_end or y != y_end:
            if x == x_end:
                y += 1
                self.decks_ship.append(Deck(x, y))
            elif y == y_end:
                x += 1
                self.decks_ship.append(Deck(x, y))
        return self.decks_ship

    def hit_in_deck(self, deck):
        self._kill_deck(deck)
        return "Hit!"

    @staticmethod
    def miss_in_ship():
        return "Miss!"

    def sunk_ship(self, deck):
        self._kill_deck(deck)
        return "Sunk!"

    def check_sunk(self):
        if self.decks.count(None) == len(self.decks) - 1:
            self.is_drowned = True
        return self.is_drowned


class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive
