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
        self.decks = [(start[0], start[1] + i) if start[1] != end[1]
                      else (start[0] + i, start[1])
                      for i in range((end[1] - start[1] + 1)
                                     + (end[0] - start[0]))]

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck == (row, column):
                self.fire(row, column)
                break

    def fire(self, row: int, column: int) -> None:
        deck_exemplar = Deck(row, column)
        if deck_exemplar.is_alive:
            deck_exemplar.is_alive = False
            self.decks.remove((row, column))
            if len(self.decks) == 0:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[deck] = new_ship

    def fire(self, location: tuple) -> str:
        for key, value in self.field.items():
            if key == location:
                value.get_deck(location[0], location[1])
                if value.is_drowned:
                    return "Sunk!"
                elif Deck(location[0], location[1]).is_alive:
                    return "Hit!"
                return "Miss!"
        return "Miss!"
