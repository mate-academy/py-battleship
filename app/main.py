class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False
                 ) -> None:
        self.ship = []
        if start == end:
            self.ship.extend([Deck(*start)])
        elif start[1] != end[1]:
            for deck in range(start[1], end[1] + 1):
                self.ship.append(Deck(start[0], deck))
        elif start[0] != end[0]:
            for deck in range(start[0], end[0] + 1):
                self.ship.append(Deck(deck, start[1]))
        self.is_drowned = is_drowned

    def fire(self, row: int, column: int) -> str:
        for deck in self.ship:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        if True not in [deck.is_alive for deck in self.ship]:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            for deck in ship.ship:
                if deck.row == location[0] and deck.column == location[1]:
                    return ship.fire(*location)
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
                if deck.is_alive is False:
                    matrix[deck.row][deck.column] = "*"
                else:
                    matrix[deck.row][deck.column] = "□"
        result = ""
        for row in matrix:
            result += "  ".join(row) + "\n"
        return result

    def _validate_field(self) -> bool:
        real = {4: 0, 3: 0, 2: 0, 1: 0}
        must_be = {4: 1, 3: 2, 2: 3, 1: 4}
        if len(self.ships) != 10:
            return False
        for ship in self.ships:
            print(len(ship.ship))
            real[len(ship.ship)] += 1
        return real == must_be
