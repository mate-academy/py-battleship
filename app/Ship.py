from typing import Tuple, List


class Ship:

    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_deck()

    def get_deck(self) -> List[Tuple[int, int]]:
        decks = []
        for row in range(self.start[0], self.end[0] + 1):
            for col in range(self.start[1], self.end[1] + 1):
                decks.append((row, col))
        return decks

    def fire(self, row: int, column: int) -> bool:
        if (row, column) in self.decks:
            self.decks.remove((row, column))
            if not self.decks:
                self.is_drowned = True
            return True
        return False
