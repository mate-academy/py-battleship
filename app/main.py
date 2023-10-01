class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.ship = []
        if start == end:
            self.ship.extend([Deck(start[0], start[1])])
        elif start[1] != end[1]:
            self.ship.extend([Deck(start[0], deck) for deck in range(start[1], end[1] + 1)])
        elif start[0] != end[0]:
            self.ship.extend([Deck(deck, start[1]) for deck in range(start[0], end[0] + 1)])
        self.is_drowned = is_drowned

    def fire(self, row, column):
        for deck in self.ship:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                self.ship.remove(deck)
        if len(self.ship) == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"

class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            for deck in ship.ship:
                if deck.row == location[0] and deck.column == location[1]:
                    return ship.fire(location[0], location[1])
        return "Miss!"

    def __repr__(self) -> str:

        matrix = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]]
        for ship in self.ships:
            for deck in ship.ship:
                matrix[deck.row][deck.column] = "□"
        result = ""
        for row in matrix:
            result += "  ".join(row) + "\n"
        return result

    def validate_field(self) -> bool:
        real = {4: 0, 3: 0, 2: 0, 1: 0}
        must_be = {4: 1, 3: 2, 2: 3, 1: 4}
        if len(self.ships) != 10:
            return False
        for ship in self.ships:
            print(len(ship.ship))
            real[len(ship.ship)] += 1
        return real == must_be
