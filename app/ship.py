from app.constants import SHIP_AFLOAT, SHIP_DROWNED
from app.deck import Deck
from app.types_aliases import Cell


class Ship:
    def __init__(self, start: Cell, end: Cell) -> None:
        self.decks: list[Deck] = []

        start_row, start_col = start
        end_row, end_col = end

        if start_row != end_row and start_col != end_col:
            raise ValueError(
                "Ship must be placed horizontally or vertically"
            )

        start_row, end_row = sorted((start_row, end_row))
        start_col, end_col = sorted((start_col, end_col))

        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                position = (start_row, col)
                self.decks.append(Deck(position=position))
        else:
            for row in range(start_row, end_row + 1):
                position = (row, start_col)
                self.decks.append(Deck(position=position))

    @property
    def size(self) -> int:
        return len(self.decks)

    @property
    def is_drowned(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)

    def hit(self, position: Cell) -> None:
        self.get_deck(position).hit()

    def get_deck(self, position: Cell) -> Deck:
        for deck in self.decks:
            if deck.position == position:
                return deck
        raise ValueError(f"Deck not found at position {position}")

    def __repr__(self) -> str:
        status = SHIP_DROWNED if self.is_drowned else SHIP_AFLOAT
        return f'Ship(size={self.size}, status="{status}")'
