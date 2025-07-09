class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self._row = row
        self._column = column
        self._is_alive = is_alive

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self._is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self._is_drowned = is_drowned
        self._decks = []
        self._creation_deck(start, end)
        self._is_horizontal = self._is_horizontal_(start, end)

    @property
    def is_drowned(self) -> bool:
        return self._is_drowned

    @property
    def decks(self) -> list[Deck]:
        return self._decks

    @property
    def is_horizontal(self) -> bool:
        return self._is_horizontal

    def _is_horizontal_(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> bool:
        return start[0] == end[0] and start[1] != end[1]

    def _creation_deck(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        deck_x = abs(start[0] - end[0])
        deck_y = abs(start[1] - end[1])

        is_straight = deck_x == 0 or deck_y == 0
        length = max(deck_y, deck_x) + 1

        if 1 <= length <= 4 and is_straight:
            for coordinate_x in range(start[0], end[0] + 1):
                for coordinate_y in range(start[1], end[1] + 1):
                    self._decks.append(Deck(coordinate_x, coordinate_y))
        else:
            print(f"Invalid ship: {(start, end)}")

    def get_deck(self, row: int, column: int) -> Deck:
        return next(
            (
                deck for deck in self._decks
                if deck.row == row and deck.column == column
            ),
            None
        )

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is None:
            return False
        else:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self._decks):
                self._is_drowned = True
                return True
            return True
