class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.col = column
        self.is_alive = is_alive
        self._sign = u"\u25A1"
