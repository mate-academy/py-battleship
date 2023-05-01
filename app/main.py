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
        ship_length = abs(sum(start) - sum(end)) + 1
        decks = []
        for i in range(ship_length):
            if start[1] < end[1]:
                decks.append(Deck(row=start[0], column=start[1] + i))
            if start[0] < end[0]:
                decks.append(Deck(row=start[0] + i, column=start[1]))
            if start[0] == end[0] and start[1] == end[1]:
                decks.append(Deck(row=start[0], column=start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        ruined_deck = self.get_deck(row, column)
        ruined_deck.is_alive = False
        deck_status = [deck.is_alive for deck in self.decks]
        if not any(deck_status):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            battleship = Ship(start=ship[0], end=ship[1])
            for deck in battleship.decks:
                key = (deck.row, deck.column)
                self.field[key] = battleship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
