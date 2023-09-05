class Deck:
    list_of_decks = {}

    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

        self.list_of_decks[(self.row, self.column)] = self
