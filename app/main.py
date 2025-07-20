class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        if start[0] == end[0]:
            self.decks = [Deck(start[0], i) for i
                          in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            self.decks = [Deck(i, start[1]) for i
                          in range(start[0], end[0] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        alive = 0
        for deck in self.decks:
            if deck.is_alive:
                alive += 1
        if alive == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship : Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:

        for key, value in self.field.items():
            if (key[0][0] <= location[0] <= key[1][0]
                    and key[0][1] <= location[1] <= key[1][1]):
                result = value.fire(location[0], location[1])
                return result

        return "Miss!"
