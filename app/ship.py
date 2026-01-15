class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:

        if start[0] == end[0]:
            self.decks = [Deck(start[0], y)
                          for y in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            self.decks = [Deck(x, start[1])
                          for x in range(start[0], end[0] + 1)]
        else:
            return

        self.start = (start[0] - 1, start[1] - 1)
        self.end = (end[0] + 1, end[1] + 1)

        self.is_drowned = is_drowned

    def get_length(self) -> int:
        return len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is not None and deck.is_alive:
            deck.is_alive = False

            for deck in self.decks:
                if deck.is_alive:
                    return "Hit!"

            self.is_drowned = True
            return "Sunk!"
        return "Already dead"

    def __eq__(self, other: any) -> bool:
        if self.start[0] <= other.start[0] and self.start[1] >= other.start[1]:
            if self.end[0] >= other.start[0] and self.end[1] <= other.end[1]:
                return True

        return False
