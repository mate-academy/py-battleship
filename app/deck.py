from dataclasses import dataclass

from app.constants import DECK_ALIVE, DECK_HIT
from app.types_aliases import Cell


@dataclass(slots=True)
class Deck:
    position: Cell
    is_alive: bool = True

    @property
    def row(self) -> int:
        return self.position[0]

    @property
    def col(self) -> int:
        return self.position[1]

    def hit(self) -> None:
        if self.is_alive:
            self.is_alive = False

    def __repr__(self) -> str:
        status = DECK_ALIVE if self.is_alive else DECK_HIT
        return f'Deck(row={self.row}, col={self.col}, status="{status}")'
