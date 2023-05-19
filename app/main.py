class Deck:
    def __init__(
            self,
            row: str,
            column: str,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.place_ship_decks(start, end)

    def place_ship_decks(self, start: tuple, end: tuple) -> list:
        decks = []
        for row_index in range(start[0], end[0] + 1):
            for col_index in range(start[1], end[1] + 1):
                decks.append(Deck(row=row_index, column=col_index))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        ruined_deck = self.get_deck(row, column)
        if ruined_deck is not None:
            ruined_deck.is_alive = False
            deck_status = [deck.is_alive for deck in self.decks]
            self.is_drowned = not any(deck_status)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            battleship = Ship(start=ship[0], end=ship[1])
            for deck in battleship.decks:
                coords = (deck.row, deck.column)
                self.field[coords] = battleship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
