class InvalidInput(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [Deck(x, y)
                      for x in range(start[0], end[0] + 1)
                      for y in range(start[1], end[1] + 1)]
        self.length = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        hit_deck = self.get_deck(row, column)
        hit_deck.is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self._validate_field(ships)
        self.ships = [Ship(*ship) for ship in ships]
        self.field = [["~" for _ in range(10)] for _ in range(10)]

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise InvalidInput("The number of ships must be 10")
        ships_count = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }
        for ship in ships:
            if ship[0][0] != ship[1][0]:
                ships_count[ship[1][0] - ship[0][0] + 1] += 1
            else:
                ships_count[ship[1][1] - ship[0][1] + 1] += 1
        if not all((ships_count[1] == 4,
                    ships_count[2] == 3,
                    ships_count[3] == 2,
                    ships_count[4] == 1)):
            raise InvalidInput(("There have to be:\n"
                                "4 1-deck ships\n"
                                "3 2-deck ships\n"
                                "2 3-deck ships\n"
                                "1 4-deck ship\n"))

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            if all((location[0] in range(ship.start[0], ship.end[0] + 1),
                    location[1] in range(ship.start[1], ship.end[1] + 1))):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for ship in self.ships:
            if not ship.is_drowned:
                for deck in ship.decks:
                    if deck.is_alive:
                        self.field[deck.row][deck.column] = u"\u25A1"
                    else:
                        self.field[deck.row][deck.column] = "*"
            else:
                for deck in ship.decks:
                    self.field[deck.row][deck.column] = "x"

        for row in self.field:
            print(*row, sep="       ")
