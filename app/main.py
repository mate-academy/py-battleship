
class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start[1] != end[1]:
            for index in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], index))
        if start[0] != end[0]:
            for index in range(start[0], end[0] + 1):
                self.decks.append(Deck(index, end[1]))
        if start[1] == end[1] and start[0] == end[0]:
            for index in range(start[0], end[0] + 1):
                self.decks.append(Deck(index, end[1]))

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
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = ships
        for ship in self.ships:
            battle_ship = Ship(start=ship[0], end=ship[1])
            for deck in battle_ship.decks:
                key = (deck.row, deck.column)
                self.field[key] = battle_ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
