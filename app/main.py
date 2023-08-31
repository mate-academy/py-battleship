import pprint


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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> dict:
        if self.start == self.end:
            return {self.start: Deck(*self.start)}
        decks = [(x, y) for x in range(self.start[0], self.end[0] + 1)
                 for y in range(self.start[1], self.end[1] + 1)]
        return {deck: Deck(*deck) for deck in decks}

    def fire(self, row: tuple, column: tuple) -> bool:
        self.decks[(row, column)].is_alive = False
        if sum([item.is_alive for item in self.decks.values()]) == 0:
            self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(*ship) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            for deck in ship.decks.keys():
                if location == deck:
                    if ship.fire(*deck):
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.field.values():
            if not ship.is_drowned:
                for index, deck in ship.decks.items():
                    if deck.is_alive:
                        field[index[0]][index[1]] = "□"
                    else:
                        field[index[0]][index[1]] = "*"
            else:
                for index, deck in ship.decks.items():
                    field[index[0]][index[1]] = "x"
        pprint.pprint(field)
